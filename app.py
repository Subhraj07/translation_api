from fastapi import FastAPI
import uvicorn
import json

with open("translated_dict.json", 'r') as f:
    en_es_dict = json.load(f)
        
es_en_dict = dict([(value, key) for key, value in en_es_dict.items()])

app = FastAPI()

def chk_word_in_dict(word, dictr):
    ret = False
    if word in dictr.keys():
        ret = True
    return ret

def get_eng_trans_data(word):
    if chk_word_in_dict(word, en_es_dict):
        return en_es_dict[str(word)]
    else:
        return "word is not available in the database"
    
def get_spanish_trans_data(word):
    if chk_word_in_dict(word, es_en_dict):
        return es_en_dict[str(word)]
    else:
        return "word is not available in the database"

@app.get("/")
async def details():
    try:
        return {
            "message1" : "please check /en-es for english and /es-en for spanish words translations",
            "en-es example" : "/en-es?words=one for single word translation , /en-es?words=one,two,hi for multiple word translation",
            "es-en example" : "/es-en?words=desgranadocaso for single word translation , /es-en?words=desgranadocaso,laborables for multiple word translation"
            }
    
    except:
        return {"message" : "Server Error occured"}
    
@app.get("/en-es")
async def en_es(words: str = ""):
    try:
        word_list = words.split(",")
        translated_res = list(map(get_eng_trans_data, word_list))
        
        return dict(zip(word_list, translated_res))
    
    except Exception as e:
        return { "error details" : str(e) }
        
@app.get("/es-en")
async def es_en(words: str = ""):
    try:
        word_list = words.split(",")
        translated_res = list(map(get_spanish_trans_data, word_list))
        
        return dict(zip(word_list, translated_res))
    
    except Exception as e:
        return { "error details" : str(e) }
    
    
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")