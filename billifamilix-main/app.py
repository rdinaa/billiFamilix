import gradio as gr
from utils.bedrock import call_bedrock
from utils.compare_vdb import compare_code_based_on_description


# coface colors: #00a787, #214269
theme = gr.themes.Default(primary_hue="blue").set(
    button_primary_background_fill_hover="#00a787",
    button_primary_background_fill_hover_dark="#00a787",
    button_primary_text_color="#214269",
    slider_color="#214269"
)

# gradio app to load the vector store
app1 = gr.Interface(fn=call_bedrock,
                    inputs=gr.Textbox(label="Insert the code segment for analysis"),
                    outputs=gr.Textbox(label="Code segment description", value=''))

# this is a placehoder for now
app2 = gr.Interface(fn=compare_code_based_on_description,
                    inputs=gr.Textbox(label="What do you want to compare"),
                    outputs=[
                        gr.Textbox(label="FAM code description", value=''),
                        gr.Textbox(label="BILLI code description", value=''),
                        gr.Textbox(label="Differences", value=''),
                        ])

with gr.Blocks(theme=theme) as demo:
    gr.TabbedInterface([app1, app2],
                       ["Code Exploration", "Compare code"],
                       css="")
    if __name__ == "__main__":
        demo.launch()

# demo = gr.TabbedInterface([app1, app2], ["Code Exploration", "Placeholder"])
# demo.launch()


