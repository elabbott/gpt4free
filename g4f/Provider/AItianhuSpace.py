from __future__ import annotations

import time
import random

from ..typing import CreateResult, Messages
from .base_provider import BaseProvider
from .helper import WebDriver, format_prompt, get_browser
from .. import debug

class AItianhuSpace(BaseProvider):
    url = "https://chat3.aiyunos.top/"
    working = True
    supports_gpt_35_turbo = True
    _domains = ["aitianhu.com", "aitianhu1.top"]

    @classmethod
    def create_completion(
        cls,
        model: str,
        messages: Messages,
        stream: bool,
        domain: str = None,
        proxy: str = None,
        timeout: int = 120,
        browser: WebDriver = None,
        headless: bool = True,
        **kwargs
    ) -> CreateResult:
        if not model:
            model = "gpt-3.5-turbo"
        if not domain:
            chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
            rand = ''.join(random.choice(chars) for _ in range(6))
            domain = random.choice(cls._domains)
            domain = f"{rand}.{domain}"
        if debug.logging:
            print(f"AItianhuSpace | using domain: {domain}")
        url = f"https://{domain}"
        prompt = format_prompt(messages)
        driver = browser if browser else get_browser("", headless, proxy)

        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        wait = WebDriverWait(driver, timeout)

        # Bypass devtools detection
        driver.get("https://blank.page/")
        wait.until(EC.visibility_of_element_located((By.ID, "sheet")))
        driver.execute_script(f"""
document.getElementById('sheet').addEventListener('click', () => {{
    window.open('{url}', '_blank');
}});
""")
        driver.find_element(By.ID, "sheet").click()
        time.sleep(10)

        original_window = driver.current_window_handle
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.close()
                driver.switch_to.window(window_handle)
                break

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea.n-input__textarea-el")))

        try:
            # Add hook in XMLHttpRequest
            script = """
const _http_request_open = XMLHttpRequest.prototype.open;
window._last_message = window._message = "";
window._loadend = false;
XMLHttpRequest.prototype.open = function(method, url) {
    if (url == "/api/chat-process") {
        this.addEventListener("progress", (event) => {
            const lines = this.responseText.split("\\n");
            try {
                window._message = JSON.parse(lines[lines.length-1])["text"];
            } catch(e) { }
        });
        this.addEventListener("loadend", (event) => {
            window._loadend = true;
        });
    }
    return _http_request_open.call(this, method, url);
}
"""
            driver.execute_script(script)

            # Input and submit prompt
            driver.find_element(By.CSS_SELECTOR, "textarea.n-input__textarea-el").send_keys(prompt)
            driver.find_element(By.CSS_SELECTOR, "button.n-button.n-button--primary-type.n-button--medium-type").click()

            # Yield response
            while True:
                chunk = driver.execute_script("""
if (window._message && window._message != window._last_message) {
    try {
        return window._message.substring(window._last_message.length);
    } finally {
        window._last_message = window._message;
    }
}
if (window._loadend) {
    return null;
}
return "";
""")
                if chunk:
                    yield chunk
                elif chunk != "":
                    break
                else:
                    time.sleep(0.1)
        finally:
            if not browser:
                driver.close()
                time.sleep(0.1)
                driver.quit()