# utils/colors.py


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    @classmethod
    def colorize(cls, text: str, color: str) -> str:
        color_code = getattr(cls, color.upper(), '')
        return f"{color_code}{text}{cls.END}"

    @classmethod
    def error(cls, text: str) -> str:
        """에러 메시지 포맷팅"""
        return cls.colorize(text, 'RED')

    @classmethod
    def success(cls, text: str) -> str:
        """성공 메시지 포맷팅"""
        return cls.colorize(text, 'GREEN')

    @classmethod
    def info(cls, text: str) -> str:
        """정보 메시지 포맷팅"""
        return cls.colorize(text, 'CYAN')

    @classmethod
    def warning(cls, text: str) -> str:
        """경고 메시지 포맷팅"""
        return cls.colorize(text, 'YELLOW')
    @staticmethod
    def format_message(role: str, content: str) -> str:
        """메시지 형식화
        Args:
            role: 메시지 작성자 역할 ('user' 또는 'assistant')
            content: 메시지 내용
        Returns:
            형식화된 메시지 문자열
        """
        if role == "user":
            return f"{Colors.BLUE} You: {Colors.END}{content}"
        return f"{Colors.GREEN}Assistant: {Colors.END}{content}"
