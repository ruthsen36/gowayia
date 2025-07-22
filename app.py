from google_search_results import GoogleSearch
from transformers import pipeline
import gradio as gr
import os

# Use variável de ambiente para a chave SerpAPI
SERP_API_KEY = os.getenv("SERP_API_KEY", "c250c4f6424506be15253c10c41d21ed6586934d6c8e5ae6a9cf217789613c3e")

# Inicializa o pipeline de resumo
summarizer = pipeline("summarization")

def goway_ia_interface(query):
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERP_API_KEY,
        "num": 3,
        "hl": "pt"
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    snippets = []
    for r in results.get("organic_results", [])[:3]:
        snippet = r.get("snippet", "")
        if snippet:
            snippets.append(snippet)

    full_text = " ".join(snippets)

    # Faz resumo do texto coletado
    try:
        summary = summarizer(full_text, max_length=150, min_length=30, do_sample=False)[0]["summary_text"]
    except Exception:
        summary = full_text

    # Código Java básico gerado (exemplo)
    java_code = f"""
// Código gerado para: {query}
public class MainActivity extends AppCompatActivity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }}
}}
    """.strip()

    # Código XML básico gerado (exemplo)
    xml_code = """
<!-- layout XML exemplo -->
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <Button
        android:id="@+id/bt_login"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Login" />

</RelativeLayout>
    """.strip()

    return (
        f"🔎 **Resumo da pesquisa:**\n{summary}",
        f"💡 **Java:**\n```java\n{java_code}\n```",
        f"📱 **XML:**\n```xml\n{xml_code}\n```"
    )

iface = gr.Interface(
    fn=goway_ia_interface,
    inputs=gr.Textbox(label="Comando para GoWay IA"),
    outputs=[
        gr.Markdown(label="Resumo da Web"),
        gr.Markdown(label="Código Java"),
        gr.Markdown(label="Layout XML")
    ],
    title="🤖 GoWay IA - Gerador de Apps Inteligente",
    description="Digite um comando como: 'Criar app de mobilidade com login e mapa'. A IA buscará informações e gerará o código inicial."
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
