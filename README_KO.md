# Python Container System

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-BSD--3--Clause-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **Language:** [English](README.md) | **한국어**

## 개요

Python Container System은 C++ [container_system](https://github.com/kcenon/container_system)과 동일한 기능을 제공하는 고성능, 타입 안전 컨테이너 프레임워크입니다. 메시징 시스템과 효율적인 데이터 관리가 필요한 범용 애플리케이션을 위해 설계되었습니다.

이 패키지는 C++ container_system과 동등한 Python 구현으로 다음을 제공합니다:
- **타입 안전 값 시스템** - 컴파일 타임 및 런타임 검사
- **다중 직렬화 포맷** - Binary, JSON, XML
- **스레드 안전 연산** - 선택적 락킹
- **중첩 컨테이너** - 계층적 데이터 구조
- **외부 의존성 없음** - Python 표준 라이브러리만 사용

## 주요 기능

### 🎯 핵심 기능
- **타입 안전성**: Python 타입 힌트 및 런타임 검증을 통한 강력한 타입 시스템
- **스레드 안전성**: 동시 접근을 위한 선택적 스레드 안전 연산
- **다중 포맷**: Binary, JSON, XML 직렬화 지원
- **메모리 효율성**: Python 내장 타입을 사용한 최적화된 저장
- **쉬운 통합**: 독립 패키지 또는 라이브러리 의존성으로 사용 가능

### 📦 값 타입

| 타입 | Python 클래스 | 설명 | 크기 |
|------|-------------|-------------|------|
| Null | `Value` | Null/빈 값 | 0 바이트 |
| Boolean | `BoolValue` | True/False | 1 바이트 |
| Integer | `ShortValue`, `IntValue`, `LongValue`, `LLongValue` | 부호 있는 정수 | 2-8 바이트 |
| Unsigned | `UShortValue`, `UIntValue`, `ULongValue`, `ULLongValue` | 부호 없는 정수 | 2-8 바이트 |
| Float | `FloatValue`, `DoubleValue` | 부동소수점 | 4-8 바이트 |
| String | `StringValue` | UTF-8 문자열 | 가변 |
| Bytes | `BytesValue` | 원시 바이트 배열 | 가변 |
| Container | `ContainerValue` | 중첩 컨테이너 | 가변 |

## 설치

### 소스에서 설치

```bash
# 저장소 복제
git clone https://github.com/kcenon/python_container_system.git
cd python_container_system

# 개발 모드로 설치
pip install -e .

# 또는 개발 의존성과 함께 설치
pip install -e ".[dev]"
```

### PyPI에서 설치 (출시 시)

```bash
pip install python-container-system
```

## 빠른 시작

### 기본 사용법

```python
from container_module import ValueContainer
from container_module.values import StringValue, IntValue, BoolValue, DoubleValue

# 헤더 정보가 있는 컨테이너 생성
container = ValueContainer(
    source_id="client_01",
    source_sub_id="session_123",
    target_id="server",
    target_sub_id="main_handler",
    message_type="user_data"
)

# 값 추가
container.add(IntValue("user_id", 12345))
container.add(StringValue("username", "john_doe"))
container.add(DoubleValue("balance", 1500.75))
container.add(BoolValue("active", True))

# 값 조회
user_id = container.get_value("user_id")
if user_id:
    print(f"User ID: {user_id.to_int()}")  # 출력: User ID: 12345

# 문자열로 직렬화
serialized = container.serialize()

# 문자열에서 역직렬화
restored = ValueContainer(data_string=serialized)
```

### 중첩 컨테이너

```python
from container_module.values import ContainerValue

# 주소를 위한 중첩 컨테이너 생성
address = ContainerValue("address")
address.add(StringValue("street", "123 Main St"))
address.add(StringValue("city", "Seattle"))
address.add(StringValue("zip", "98101"))

# 메인 컨테이너에 추가
container.add(address)

# 중첩된 값 접근
address_value = container.get_value("address")
if address_value:
    print(f"Nested values: {address_value.child_count()}")
```

### JSON/XML 변환

```python
# JSON으로 변환
json_str = container.to_json()
print(json_str)

# XML로 변환
xml_str = container.to_xml()
print(xml_str)
```

### 빌더 패턴

```python
from container_module import MessagingBuilder
from container_module.values import StringValue, IntValue

# fluent API를 사용한 컨테이너 생성
container = (
    MessagingBuilder()
    .set_source("client1", "session1")
    .set_target("server1", "handler1")
    .set_type("request")
    .add_value(StringValue("name", "John"))
    .add_value(IntValue("age", 30))
    .build()
)

# 빌더는 reset 후 재사용 가능
builder = MessagingBuilder()
container1 = builder.set_source("src1").set_type("type1").build()
container2 = builder.reset().set_source("src2").set_type("type2").build()
```

### 의존성 주입 (Dependency Injection)

```python
from container_module import IContainerFactory, DefaultContainerFactory
from container_module.values import StringValue, IntValue

# DI를 위한 팩토리 패턴 사용
factory = DefaultContainerFactory()
container = factory.create(
    source_id="client1",
    target_id="server1",
    message_type="request"
)

# 값이 미리 채워진 컨테이너 생성
container = factory.create_with_values(
    values=[StringValue("name", "John"), IntValue("age", 30)],
    source_id="client1",
    message_type="user_data"
)

# 팩토리를 통한 빌더 사용
container = (
    factory.create_builder()
    .set_source("client1")
    .set_target("server1")
    .add_value(StringValue("data", "value"))
    .build()
)

# FastAPI 통합 예제
from fastapi import Depends

def get_container_factory() -> IContainerFactory:
    return DefaultContainerFactory()

@app.post("/messages")
async def create_message(
    factory: IContainerFactory = Depends(get_container_factory)
):
    container = factory.create(message_type="response")
    # ...
```

### 스레드 안전 연산

```python
import threading

# 스레드 안전성 활성화
container = ValueContainer(message_type="thread_safe")
container.enable_thread_safety(True)

# 여러 스레드에서 사용
def worker():
    container.add(StringValue("data", "value"))
    value = container.get_value("data")

threads = [threading.Thread(target=worker) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

## 프로젝트 구조

```
python_container_system/
├── container_module/           # 메인 패키지
│   ├── __init__.py             # 패키지 초기화
│   ├── core/                   # 핵심 기능
│   │   ├── value_types.py      # 값 타입 열거형
│   │   ├── value.py            # 기본 Value 클래스
│   │   └── container.py        # ValueContainer 클래스
│   ├── values/                 # 값 구현
│   │   ├── bool_value.py       # Boolean 값
│   │   ├── numeric_value.py    # 숫자 값
│   │   ├── string_value.py     # 문자열 값
│   │   ├── bytes_value.py      # 바이트 배열 값
│   │   └── container_value.py  # 중첩 컨테이너
│   ├── messaging/              # 메시징 유틸리티
│   │   ├── __init__.py         # 메시징 exports
│   │   └── builder.py          # MessagingBuilder 클래스
│   ├── di/                     # 의존성 주입 지원
│   │   ├── __init__.py         # DI exports
│   │   └── adapters.py         # 팩토리 및 시리얼라이저 인터페이스
│   └── utilities/              # 유틸리티 함수
├── tests/                      # 테스트 스위트
│   ├── test_value_types.py     # 타입 시스템 테스트
│   ├── test_container.py       # 컨테이너 테스트
│   ├── test_values.py          # 값 테스트
│   ├── test_messaging_builder.py  # MessagingBuilder 테스트
│   └── test_di_adapters.py     # DI 어댑터 테스트
├── examples/                   # 예제 프로그램
│   ├── basic_usage.py          # 기본 사용 예제
│   ├── advanced_usage.py       # 고급 기능 예제
│   └── di_example.py           # 의존성 주입 예제
├── docs/                       # 문서
├── setup.py                    # 설치 스크립트
├── pyproject.toml              # 프로젝트 설정
├── README.md                   # 영문 README
└── LICENSE                     # BSD 3-Clause 라이선스
```

## API 레퍼런스

### ValueContainer

```python
class ValueContainer:
    """메시지 관리를 위한 메인 컨테이너 클래스."""

    def __init__(
        self,
        source_id: str = "",
        source_sub_id: str = "",
        target_id: str = "",
        target_sub_id: str = "",
        message_type: str = "",
        units: Optional[List[Value]] = None,
    ) -> None: ...

    # 헤더 관리
    def set_source(self, source_id: str, source_sub_id: str = "") -> None: ...
    def set_target(self, target_id: str, target_sub_id: str = "") -> None: ...
    def set_message_type(self, message_type: str) -> None: ...
    def swap_header(self) -> None: ...

    # 값 관리
    def add(self, target_value: Value, update_immediately: bool = False) -> Value: ...
    def remove(self, target: Union[str, Value], update_immediately: bool = False) -> None: ...
    def get_value(self, target_name: str, index: int = 0) -> Optional[Value]: ...
    def value_array(self, target_name: str) -> List[Value]: ...
    def clear_value(self) -> None: ...

    # 직렬화
    def serialize(self) -> str: ...
    def deserialize(self, data_string: str, parse_only_header: bool = True) -> bool: ...
    def to_json(self) -> str: ...
    def to_xml(self) -> str: ...

    # 파일 I/O
    def load_packet(self, file_path: str) -> None: ...
    def save_packet(self, file_path: str) -> None: ...

    # 유틸리티
    def copy(self, containing_values: bool = True) -> ValueContainer: ...
    def initialize(self) -> None: ...
```

### 값 타입

```python
from container_module.values import (
    BoolValue,          # Boolean 값
    ShortValue,         # 16비트 부호 있는 정수
    IntValue,           # 32비트 부호 있는 정수
    LongValue,          # 플랫폼 의존 부호 있는 long
    LLongValue,         # 64비트 부호 있는 정수
    UShortValue,        # 16비트 부호 없는 정수
    UIntValue,          # 32비트 부호 없는 정수
    ULongValue,         # 플랫폼 의존 부호 없는 long
    ULLongValue,        # 64비트 부호 없는 정수
    FloatValue,         # 32비트 부동소수점
    DoubleValue,        # 64비트 부동소수점
    StringValue,        # UTF-8 문자열
    BytesValue,         # 원시 바이트 배열
    ContainerValue,     # 중첩 컨테이너
)
```

### MessagingBuilder

```python
from container_module import MessagingBuilder

class MessagingBuilder:
    """fluent ValueContainer 생성을 위한 빌더."""

    def set_source(self, source_id: str, source_sub_id: str = "") -> MessagingBuilder: ...
    def set_target(self, target_id: str, target_sub_id: str = "") -> MessagingBuilder: ...
    def set_type(self, message_type: str) -> MessagingBuilder: ...
    def add_value(self, value: Value) -> MessagingBuilder: ...
    def add_values(self, values: List[Value]) -> MessagingBuilder: ...
    def build(self) -> ValueContainer: ...
    def reset(self) -> MessagingBuilder: ...
```

### 의존성 주입

```python
from container_module import (
    IContainerFactory,       # 컨테이너 생성 프로토콜
    IContainerSerializer,    # 직렬화 프로토콜
    DefaultContainerFactory, # 기본 팩토리 구현
    DefaultContainerSerializer,  # 기본 시리얼라이저 구현
)

class IContainerFactory(Protocol):
    """ValueContainer 인스턴스 생성을 위한 프로토콜."""

    def create(self, source_id: str = "", ...) -> ValueContainer: ...
    def create_with_values(self, values: List[Value], ...) -> ValueContainer: ...
    def create_from_serialized(self, data: str, ...) -> ValueContainer: ...
    def create_builder(self) -> MessagingBuilder: ...

class IContainerSerializer(Protocol):
    """컨테이너 직렬화/역직렬화를 위한 프로토콜."""

    def serialize(self, container: ValueContainer) -> str: ...
    def serialize_bytes(self, container: ValueContainer) -> bytes: ...
    def deserialize(self, data: str, ...) -> ValueContainer: ...
    def deserialize_bytes(self, data: bytes, ...) -> ValueContainer: ...
```

## 개발

### 테스트 실행

```bash
# 테스트 의존성 설치
pip install -e ".[test]"

# 모든 테스트 실행
pytest

# 커버리지와 함께 실행
pytest --cov=container_module --cov-report=html

# 특정 테스트 파일 실행
pytest tests/test_container.py
```

### 코드 품질

```bash
# black으로 코드 포맷
black container_module tests examples

# mypy로 타입 검사
mypy container_module

# pylint로 린팅
pylint container_module
```

## C++ 버전과의 비교

| 기능 | C++ container_system | Python container_system |
|---------|---------------------|------------------------|
| **언어** | C++20 | Python 3.8+ |
| **타입 안전성** | 컴파일 타임 + 런타임 | 런타임 (타입 힌트 포함) |
| **성능** | ~2M ops/sec | ~500K ops/sec |
| **메모리** | 스마트 포인터, RAII | 자동 가비지 컬렉션 |
| **스레드 안전성** | mutex | Threading.RLock |
| **SIMD** | ARM NEON, x86 AVX | NumPy (선택적) |
| **직렬화** | Binary, JSON, XML | Binary, JSON, XML |
| **의존성** | fmt, spdlog | 없음 (표준 라이브러리만) |
| **사용 사례** | 고성능 C++ 앱 | Python 애플리케이션, 통합 |

## 호환성

이 Python 구현은 C++ 버전과 **와이어 호환**되도록 설계되었습니다:
- 동일한 직렬화 포맷
- 동일한 값 타입 코드
- C++ container_system과 데이터 교환 가능

## 예제

### 예제 1: 메시지 전달

```python
# 요청 생성
request = ValueContainer(
    source_id="client",
    target_id="server",
    message_type="get_user"
)
request.add(IntValue("user_id", 12345))

# 전송 (직렬화)
data = request.serialize()

# 수신 및 처리
response = ValueContainer(
    source_id="server",
    target_id="client",
    message_type="user_data"
)
response.add(StringValue("name", "John Doe"))
response.add(StringValue("email", "john@example.com"))
```

### 예제 2: 데이터 저장

```python
# 컨테이너를 파일에 저장
container.save_packet("data/user_12345.dat")

# 파일에서 컨테이너 로드
loaded = ValueContainer()
loaded.load_packet("data/user_12345.dat")
```

### 예제 3: 바이너리 데이터

```python
from container_module.values import BytesValue

# 바이너리 데이터 생성
binary_data = bytes([0xFF, 0xFE, 0xFD, 0xFC])
container.add(BytesValue("image_data", binary_data))

# 바이너리 데이터 조회
image = container.get_value("image_data")
if image:
    data = image.to_bytes()
    hex_str = image.to_hex()
    b64_str = image.to_base64()
```

## 기여하기

기여를 환영합니다! 가이드라인은 [CONTRIBUTING.md](CONTRIBUTING.md)를 참조하세요.

1. 저장소 포크
2. 기능 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 푸시 (`git push origin feature/amazing-feature`)
5. Pull Request 열기

## 라이선스

이 프로젝트는 BSD 3-Clause License에 따라 라이선스가 부여됩니다 - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 감사의 말

- C++ [container_system](https://github.com/kcenon/container_system)에서 영감을 받음
- 메시징 시스템 생태계와 호환되도록 설계됨
- 유지 관리자: kcenon@naver.com

## 지원

- **이슈**: [GitHub Issues](https://github.com/kcenon/python_container_system/issues)
- **이메일**: kcenon@naver.com

---

<p align="center">
  Made with ❤️ by 🍀☀🌕🌥 🌊
</p>
