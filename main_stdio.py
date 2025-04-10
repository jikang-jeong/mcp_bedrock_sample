import asyncio
import os

from dotenv import load_dotenv
from mcp import StdioServerParameters

from mcp_client.client import MCPClient
from utils.colors import Colors


async def handle_resource_update(uri: str):
    """Handle updates to resources from the MCP server"""
    print(f"{Colors.YELLOW}Resource updated: {uri}{Colors.END}")
    # You could trigger a refresh of the resource here if needed


def print_tools(tools):
    """Print available tools in a nice format"""
    print(f"{Colors.CYAN}Available Tools:{Colors.END}")
    for tool in tools:
        print(f"  • {Colors.GREEN}{tool.name}{Colors.END}: {tool.description}")
    print()  # Add a blank line for spacing


def print_init():
    """Print a welcome message"""
    print('\033[2J\033[H', end='')
    print(f"{Colors.HEADER}{Colors.BOLD}Welcome to AI Assistant!{Colors.END}")
    print(f"{Colors.CYAN}I'm here to help you with any questions or tasks.{Colors.END}")
    print(f"{Colors.CYAN}Type 'quit' to exit.{Colors.END}\n")


async def main():
    # 환경 변수 로드
    load_dotenv()
    model_id = os.getenv('LLM_MODEL')
    # Create server parameters for stdio configuration
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server/server.py"],  # 상대 경로 그대로 유지
        env=None
    )
    # MCP 클라이언트 초기화 및 서버 연결
    async with MCPClient(model_id) as mcp_client:
        try:
            await mcp_client.connect_stdio(server_params)

            # 도구 가져오기 및 등록
            tools = await mcp_client.get_available_tools()
            for tool in tools:
                mcp_client.agent.tools.register_tool(
                    name=tool.name,
                    func=mcp_client.call_tool,
                    description=tool.description,
                    input_schema={'json': tool.inputSchema}
                )
            print_init()
            print_tools(tools)  # Print available tools after welcome message

            # 대화형 프롬프트 루프
            while True:
                try:
                    user_prompt = input(f"\n{Colors.BOLD}User: {Colors.END}")
                    if not user_prompt.strip():
                        continue

                        # Process the prompt and display the response
                    print(f"\n{Colors.YELLOW} Thinking...{Colors.END}")
                    response = await mcp_client.agent.invoke_with_prompt(user_prompt)
                    # ###### usage : resource ######
                    # resources = await mcp_client.read_resource("resource://db_schema")
                    # db_schema = ""
                    # for resource in resources.contents:
                    #     db_schema += resource.text
                    #
                    # response = await mcp_client.agent.invoke_with_prompt(
                    #     "db schema: " + db_schema + ",참고해서 prompt:" + user_prompt)
                    print(f"\n{Colors.format_message('assistant', response)}")

                except KeyboardInterrupt:
                    print("\nExiting...")
                    break

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
