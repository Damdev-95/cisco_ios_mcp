## Cisco IOS MCP Server

# Main Features & Capabilities

* Device Management: Uses netmiko to handle SSH sessions for device interaction, including automatic detection of prompt changes and enable-mode transitions.

* Intelligent Discovery: Tools like ping_and_learn_arp allow the AI to actively probe the network to "learn" about connected devices.

* Operational Intelligence: High-level tools for BGP, OSPF, and Routing Table analysis that return structured data for the AI to interpret.

* Safety Guardrails: A built-in regex-based Security Filter that blocks destructive commands (like reload or erase) before they reach the router.

* Resource Awareness: Uses MCP "Resources" to give the AI a persistent view of the running-config without having to re-fetch it constantly.

Step 1: Create a Project Directory
Open your terminal (or Command Prompt) and clone the repository.

```bash
git clone https://github.com/Damdev-95/cisco_ios_mcp.git
cd cisco_ios_mcp
```

# Step 2: Install Dependencies
Use the requirements.txt file 

```bash
pip install -r requirements.txt
```

# Step 3: Configure Environment Variables
locate the .env, This is where you store sensitive router credentials so they aren't hardcoded in your script.

```bash
IOS_HOST=192.168.1.1
IOS_USER=admin
IOS_PASS=Cisco123
IOS_SECRET=EnablePassword
```

# Step 4: Testing and Debugging

*  Testing & Debugging (The "Inspector")
Before connecting to Claude Desktop, use the MCP Inspector. It provides a web interface to test your tools and see the raw router output.

Run the inspector command:

```bash
mcp dev main.py
```
Open your browser to http://localhost:3000.

Try calling the show_ip_route tool to ensure your SSH connection is working.

# Integration with Claude Desktop

Open your claude_desktop_config.json.

Add the following block:

```json
{
  "mcpServers": {
    "cisco-router": {
      "command": "path/python",
      "args": ["/ABSOLUTE/PATH/TO/main.py"]
    }
  }
}
```
# Note: Use absolute paths (e.g., C:/Users/Name/... or /Users/name/...) for both the Python executable and the script to ensure Claude can find them

Use this command to check your python absoluaton location 

```bash
which python
```

See the below example 

<img width="1111" height="387" alt="image" src="https://github.com/user-attachments/assets/59927773-9d70-4341-9830-a42200ef2dbc" />

# Claude ouput

<img width="1784" height="1079" alt="image" src="https://github.com/user-attachments/assets/2c1343c0-c891-483c-b172-c8d8470cdcc1" />

## Integration with different AI IDEs

# 1. VS Code (via Claude Dev / Roo Code)
If you use extensions like Roo Code or Claude Dev in VS Code:

* Open the extension settings.
* Find the MCP Servers configuration section.
* Add the server details:

```bash
Type: command

Command: python

Args: ["/path/to/your/server.py"]
```


# 2. Cursor
Cursor has native MCP support in the Composer and Chat features:
Go to Cursor Settings > General > Features > MCP.

* Click + Add Server.
* Set the name to Cisco-Router and the type to command.
* Paste the run command: python /path/to/your/server.py.
* Restart Cursor. You can now use @Cisco-Router in the chat to trigger network actions.

# 3. Goose

* Goose (Block's open-source agent) is designed for CLI-first MCP usage:
* Open your goose configuration file (usually in ~/.goose/config.yaml).
* Add the extension entry:

```yaml
extensions:
  cisco-router:
    cmd: python
    args: ["/absolute/path/to/server.py"]
```
Run goose session. You can use Goose: "Check the interface status on the router," and it will call the Python script.




