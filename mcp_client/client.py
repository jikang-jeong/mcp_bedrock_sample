from contextlib import AsyncExitStack
from typing import Any, List, Optional

from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client

from .converse_agent import ConverseAgent
from .converse_tools import ConverseToolManager


class MCPClient:
    def __init__(self, model_id: str):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.model_id = model_id
        self.agent = ConverseAgent(model_id)
        self.agent.tools = ConverseToolManager()
        self._resource_update_handler = None
        self._resource_handlers = {}

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.exit_stack.aclose()

    async def connect_stdio(self, server_params: StdioServerParameters):
        """Establishes connection to MCP server"""
        self._client = stdio_client(server_params)
        self.read, self.write = await self._client.__aenter__()
        session = ClientSession(self.read, self.write)
        self.session = await session.__aenter__()
        await self.session.initialize()

    async def connect_to_server(self, server_url: str):
        """Connect to an MCP server"""
        try:
            sse_transport = await self.exit_stack.enter_async_context(sse_client(server_url))
            self.read, self.write = sse_transport
            self.session = await self.exit_stack.enter_async_context(ClientSession(self.read, self.write))
            await self.session.initialize()
            response = await self.session.list_tools()
            tools = response.tools
            print(f"Connected to server with tools:", [tool.name for tool in tools])
        except Exception as e:
            print(f"Error while connecting to server: {str(e)}, please check remote host URL.")
            raise


    async def get_available_tools(self) -> List[Any]:
        """Fetch available tools from the server"""
        if not self.session:
            raise RuntimeError("Not connected to server")

        response = await self.session.list_tools()
        return response.tools

    async def call_tool(self, tool_name: str, params: dict) -> Any:

        """Call a tool on the server"""
        if not self.session:
            raise RuntimeError("Not connected to server")

        return await self.session.call_tool(tool_name, params)

    async def get_available_resources(self) -> List[Any]:
        """Fetch available resources from the server"""
        if not self.session:
            raise RuntimeError("Not connected to server")

        response = await self.session.list_resources()
        return response.resources

    async def subscribe_to_resource(self, resource_uri: str):
        """특정 리소스를 구독합니다."""
        if not self.session:
            raise RuntimeError("Not connected to server")
        await self.session.subscribe_resource(resource_uri)

    async def read_resource(self, resource_uri: str):
        """리소스 값을 읽어옵니다."""
        if not self.session:
            raise RuntimeError("Not connected to server")
        return await self.session.read_resource(resource_uri)

    def on_resource_update(self, handler):
        """리소스 업데이트 핸들러를 등록합니다."""
        self._resource_handlers[handler.__name__] = handler
