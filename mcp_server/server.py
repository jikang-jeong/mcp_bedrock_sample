import psycopg
import requests
from mcp.server.fastmcp import FastMCP, Context

# Initialize FastMCP server
mcp = FastMCP(name="mcp-server")


def get_connection():
    return psycopg.connect(
        host='localhost',  # PostgreSQL 서버 주소
        dbname='postgres',  # 데이터베이스 이름
        user='postgres',  # 사용자 이름
        password='postgres'  # 비밀번호
    )


@mcp.resource("resource://db_schema", name="get_db_schema", mime_type="text/plain")
def get_db_schema() -> str:
    """데이터베이스 스키마를 리소스로 제공"""
    return """
            CREATE TABLE class (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            );

            -- 주석 추가
            COMMENT ON TABLE class IS '수업 정보를 저장하는 테이블';
            COMMENT ON COLUMN class.id IS '클래스 고유 ID';
            COMMENT ON COLUMN class.name IS '클래스 이름';

            -- 학생 테이블 생성
            CREATE TABLE student (
                id SERIAL PRIMARY KEY,
                class_id INTEGER REFERENCES class(id)
            );

            -- 주석 추가
            COMMENT ON TABLE student IS '학생 정보를 저장하는 테이블';
            COMMENT ON COLUMN student.id IS '학생 고유 ID';
            COMMENT ON COLUMN student.class_id IS '학생이 소속된 클래스 ID (class 테이블 참조)';
            """


@mcp.tool()
async def execute_query(sql: str, ctx: Context) -> str:
    """SQL 쿼리를 resource 실행"""
    # schemeResource = await ctx.read_resource(f"resource://db_schema")
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(sql)
        result = cur.fetchall()
        conn.commit()  # 데이터 변경이 있을 경우 커밋
        return "\n".join(str(row) for row in result)
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        cur.close()
        conn.close()


@mcp.tool()
async def get_wikipedia(query: str) -> str:
    """위키피디아 API로 검색 결과를 반환합니다. """
    headers = {"User-Agent": "MyWikipediaApp/1.0"}
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": 10,
        "format": "json",
        "utf8": "",
        "origin": "*"
    }

    try:
        response = requests.get(
            "https://en.wikipedia.org/w/api.php",
            headers=headers,
            params=params
        )
        response.raise_for_status()

        data = response.json()
        results = [
            {
                "title": item["title"],
                "snippet": item["snippet"],
                "pageid": item["pageid"],
                "timestamp": item["timestamp"]
            }
            for item in data.get("query", {}).get("search", [])
        ]

        return data
    except Exception as e:
        print(f"Server error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    print("Starting MCP Demo Server...")
    try:
        # Start the server
        mcp.run()
    except Exception as e:
        print(f"Server error: {e}", exc_info=True)
        raise
