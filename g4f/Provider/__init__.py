from __future__ import annotations

from .AiAsk           import AiAsk
from .Aichat          import Aichat
from .AItianhu        import AItianhu
from .AItianhuSpace   import AItianhuSpace
from .Berlin          import Berlin
from .Bing            import Bing
from .ChatAnywhere    import ChatAnywhere
from .ChatBase        import ChatBase
from .ChatForAi       import ChatForAi
from .Chatgpt4Online  import Chatgpt4Online
from .ChatgptAi       import ChatgptAi
from .ChatgptDemo     import ChatgptDemo
from .ChatgptFree     import ChatgptFree
from .ChatgptLogin    import ChatgptLogin
from .ChatgptX        import ChatgptX
from .DeepInfra       import DeepInfra
from .FakeGpt         import FakeGpt
from .FreeGpt         import FreeGpt
from .GPTalk          import GPTalk
from .GptChatly       import GptChatly
from .GptForLove      import GptForLove
from .GptGo           import GptGo
from .GptGod          import GptGod
from .Hashnode        import Hashnode
from .Koala           import Koala
from .Liaobots        import Liaobots
from .Llama2          import Llama2
from .MyShell         import MyShell
from .NoowAi          import NoowAi
from .Opchatgpts      import Opchatgpts
from .PerplexityAi    import PerplexityAi
from .Phind           import Phind
from .Vercel          import Vercel
from .Ylokh           import Ylokh
from .You             import You
from .Yqcloud         import Yqcloud
from .GeekGpt         import GeekGpt

from .base_provider  import BaseProvider, AsyncProvider, AsyncGeneratorProvider
from .retry_provider import RetryProvider
from .deprecated     import *
from .needs_auth     import *
from .unfinished     import *

import sys

__modules__: list = [
    getattr(sys.modules[__name__], provider) for provider in dir()
    if not provider.startswith("__")
]
__providers__: list[type[BaseProvider]] = [
    provider for provider in __modules__
    if isinstance(provider, type)
    and issubclass(provider, BaseProvider)
]
__all__: list[str] = [
    provider.__name__ for provider in __providers__
]
__map__: dict[str, BaseProvider] = dict([
    (provider.__name__, provider) for provider in __providers__
])

class ProviderUtils:
    convert: dict[str, BaseProvider] = __map__