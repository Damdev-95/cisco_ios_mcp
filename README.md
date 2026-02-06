## Cisco IOS MCP Server

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
## Note: Use absolute paths (e.g., C:/Users/Name/... or /Users/name/...) for both the Python executable and the script to ensure Claude can find them

Use this command to check your python absoluaton location 

```bash
which python
```

See the below example 

<img width="1111" height="387" alt="image" src="https://github.com/user-attachments/assets/59927773-9d70-4341-9830-a42200ef2dbc" />

# Claude ouput

<img width="1784" height="1079" alt="image" src="https://github.com/user-attachments/assets/2c1343c0-c891-483c-b172-c8d8470cdcc1" />


