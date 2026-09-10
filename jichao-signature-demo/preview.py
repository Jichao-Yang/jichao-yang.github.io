#!/usr/bin/env python3
"""飞书 GIF 签名的最小链接预览服务。Python 3.10+，lark-oapi==1.7.3。"""
import argparse
from getpass import getpass
from types import SimpleNamespace
from urllib.parse import urlsplit


def make_preview(url: str, title: str, image_key: str):
    def preview(event):
        if event.event.context.url != url:
            return {}
        print("收到目标链接的预览请求。", flush=True)
        return {"inline": {"title": title, "image_key": image_key}}

    return preview


def self_test():
    url = "https://example.com/animated-signature/"
    preview = make_preview(url, "签名会动", "img_example")

    def event(value):
        return SimpleNamespace(event=SimpleNamespace(context=SimpleNamespace(url=value)))

    assert preview(event(url)) == {
        "inline": {"title": "签名会动", "image_key": "img_example"}
    }
    for other in ("https://other.example/", url + "extra", url + "?test=1"):
        assert preview(event(other)) == {}
    print("自检通过：仅为完全匹配的 URL 返回标题和图片标识。")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="只检查回调，不连接飞书")
    if parser.parse_args().self_test:
        self_test()
        return

    import lark_oapi as lark

    app_id = input("App ID: ").strip()
    app_secret = getpass("App Secret（输入不会显示）: ").strip()
    url = input("签名和文章共用的完整 HTTPS URL: ").strip()
    title = input("签名显示文字: ").strip()
    image_key = input("图片 image_key: ").strip()
    parsed = urlsplit(url)
    if not app_id or not app_secret or not title:
        raise SystemExit("App ID、App Secret 和显示文字不能为空。")
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.fragment:
        raise SystemExit("请输入无账号信息、无片段标识的完整 HTTPS URL。")
    if (not image_key.startswith("img_") or image_key.endswith("_MIDDLE")
            or any(c in image_key for c in "/? \t\n")):
        raise SystemExit("请输入 imkey:// 后、问号前的原始 image_key。")

    handler = (
        lark.EventDispatcherHandler.builder("", "")
        .register_p2_url_preview_get(make_preview(url, title, image_key))
        .build()
    )
    print("正在建立长连接。可前往开放平台验证连接；按 Ctrl+C 停止。")
    try:
        lark.ws.Client(
            app_id, app_secret, event_handler=handler, log_level=lark.LogLevel.ERROR
        ).start()
    except KeyboardInterrupt:
        print("\n服务已停止。已加载的 GIF 可能继续播放，新的预览解析将不再得到本服务响应。")


if __name__ == "__main__":
    main()
