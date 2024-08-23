from dataclasses import dataclass


@dataclass
class ApiResponse:
    id: int
    message: str
