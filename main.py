import logging
import os
import re
from typing import List, Optional
from fastmcp import FastMCP
from netmiko import ConnectHandler, NetmikoAuthenticationException, NetmikoTimeoutException
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

# Initialize FastMCP
mcp = FastMCP("cisco-chat")

# Logging to stderr (standard for MCP transport)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cisco-mcp")

# --- SAFETY & UTILS ---

# List of prohibited command patterns for safety
BANNED_COMMANDS = [
    r"reload", r"erase", r"format", r"delete", r"write erase",
    r"crypto key zeroize", r"no ip routing"
]

def is_command_safe(command: str) -> bool:
    """Checks if a command contains dangerous keywords."""
    for pattern in BANNED_COMMANDS:
        if re.search(pattern, command, re.IGNORECASE):
            return False
    return True

def get_connection():
    """Helper to establish a Netmiko SSH connection."""
    return ConnectHandler(
        device_type="cisco_ios",
        host=os.getenv("IOS_HOST"),
        username=os.getenv("IOS_USER"),
        password=os.getenv("IOS_PASS"),
        secret=os.getenv("IOS_SECRET"),
    )

# --- OPERATIONAL TOOLS ---

@mcp.tool()
def show_ip_route(destination: Optional[str] = None) -> str:
    """
    Shows the routing table. Specify a destination IP to see the specific path.
    """
    cmd = f"show ip route {destination}" if destination else "show ip route"
    try:
        with get_connection() as net_connect:
            return net_connect.send_command(cmd)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def ping_and_learn_arp(target_ip: str) -> str:
    """
    Pings an IP and checks the ARP table to 'learn' its MAC address and reachability.
    """
    try:
        with get_connection() as net_connect:
            # Ping to populate ARP cache
            net_connect.send_command(f"ping {target_ip} repeat 3")
            # Extract ARP entry
            arp_table = net_connect.send_command(f"show ip arp {target_ip}")
            return f"ARP Discovery Result for {target_ip}:\n{arp_table}"
    except Exception as e:
        return f"Discovery failed: {str(e)}"

@mcp.tool()
def get_neighbor_info() -> str:
    """
    Learns about directly connected devices using CDP and LLDP.
    """
    try:
        with get_connection() as net_connect:
            cdp = net_connect.send_command("show cdp neighbors detail")
            lldp = net_connect.send_command("show lldp neighbors")
            return f"--- CDP NEIGHBORS ---\n{cdp}\n\n--- LLDP NEIGHBORS ---\n{lldp}"
    except Exception as e:
        return f"Neighbor discovery failed: {str(e)}"

@mcp.tool()
def execute_custom_show(command: str) -> str:
    """Executes any 'show' command safely."""
    if not command.strip().lower().startswith("show"):
        return "Error: This tool only accepts 'show' commands."
    
    try:
        with get_connection() as net_connect:
            return net_connect.send_command(command)
    except Exception as e:
        return f"Execution error: {str(e)}"

# --- CONFIGURATION TOOLS ---

@mcp.tool()
def apply_config(commands: List[str]) -> str:
    """
    Applies a list of configuration commands. 
    Safety filter applied to prevent destructive actions.
    """
    for cmd in commands:
        if not is_command_safe(cmd):
            return f"Security Alert: Blocked dangerous command '{cmd}'"

    try:
        with get_connection() as net_connect:
            net_connect.enable()
            output = net_connect.send_config_set(commands)
            return f"Config Success:\n{output}"
    except Exception as e:
        return f"Config Failure: {str(e)}"

# --- RESOURCES ---

@mcp.resource("cisco://state/running-config")
def resource_running_config() -> str:
    """Provides the full current running configuration."""
    with get_connection() as net_connect:
        return net_connect.send_command("show running-config")

@mcp.resource("cisco://state/interfaces")
def resource_int_brief() -> str:
    """Provides a quick summary of interface status and IPs."""
    with get_connection() as net_connect:
        return net_connect.send_command("show ip interface brief")

if __name__ == "__main__":
    mcp.run()