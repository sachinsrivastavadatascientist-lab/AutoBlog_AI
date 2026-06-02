from src.state.blogstate import BlogState
from langchain_core.prompts.chat import ChatPromptTemplate


class BlogNode:
    '''
    A class to represent the blog node
    '''

    def __init__(self,llm):
        self.llm=llm

    def title_creation(self,state:BlogState):
        '''
        create the title for the blog
        '''

        if "topic" in state and state["topic"]:
            instruction = '''
                      You are an expert blog content writer.Use Markdown formatting. 
                      Generate a blog title for the {topic}.
                      The title should be creative and SEO friendly'''
            
            prompt = ChatPromptTemplate.from_template(template = instruction)
            title_chain = prompt|self.llm

            response = title_chain.invoke({"topic":state["topic"]})

            return {"blog":{"title":response.content}}
        
    def content_generation(self,state:BlogState):

        if "topic" in state and state["topic"]:

            system_prompt ="""
                           You are asn expert blog wrtiter. Use Markdown formatting.
                           Generate the detailed blog content with detailed breakdown for the topic {topic}"""
            
            prompt = ChatPromptTemplate.from_template(template = system_prompt)
            content_chain = prompt|self.llm

            response = content_chain.invoke({"topic":state["topic"]})

            return {"blog":{"content":response.content}}
            