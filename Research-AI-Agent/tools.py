from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime

search=DuckDuckGoSearchRun()
my_search_tool=Tool(
    name="Search_Tool",
    func=search.run,
    description="Search the web for information about the given query"
)

APIWrapper=WikipediaAPIWrapper(top_k_results=5, doc_content_chars_max=100)
wiki_tool=WikipediaQueryRun(api_wrapper=APIWrapper)


def save_to_text_file(data:str, filename:str="research_output.txt"):
    timestamp=datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    formatted_text=f"---Research Output---\n{timestamp}\n{data}\n\n"

    with open(filename,"a", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"Saved to text file - {filename}"


save_to_textfile=Tool(
    name="save_to_textfile",
    func=save_to_text_file,
    description="Save structured research data to text file"
)
