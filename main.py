from cefpython3 import cefpython as cef
import platform,sys,os


def main():
    sys.excepthook = cef.ExceptHook 
    cef.DpiAware.EnableHighDpiSupport()
    cef.Initialize(settings={}, switches={'disable-gpu-compositing': None})
    url = os.getcwd().replace("\\","/") + "/ui/trans.html"
    window = cef.CreateBrowserSync(url=url,
                          window_title="Hello World!")

    bindings = cef.JavascriptBindings()
    bindings.SetFunction("alert",pyLeart)
    bindings.SetObject("external",external)
    window.SetJavascriptBindings(bindings)
    cef.MessageLoop()
    cef.Shutdown()


if __name__ == '__main__':
    main()