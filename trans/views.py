from django.shortcuts import render, redirect
import googletrans
from googletrans import Translator
from gtts import gTTS
    

# Create your views here.

def index(request):
    context={
        "ndict" : googletrans.LANGUAGES
    }

    if request.method=="POST":
        er=request.POST.get("er")
        ed=request.POST.get("ed")
        text=request.POST.get("translate")

        translator = Translator()
        trans=translator.translate(text, src=er, dest=ed)
        t = trans.text

        tts = gTTS(text=t, lang=ed)
        filename = "media/tts/trans.mp3"
        tts.save(filename)
        
        context.update({
            't' : t,
            'text' : text,
            'er' : er,
            'ed' : ed
        })
        
    return render(request, "trans/index.html", context)