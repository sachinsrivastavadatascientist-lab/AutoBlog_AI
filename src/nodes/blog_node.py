import sys
from src.state.blogstate import BlogState
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from src.state.blogstate import Blog
from src.exception import CustomException
from src.logger import logging

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
        try:
            if "topic" in state and state["topic"]:
                logging.info("Entering into title creation node")
                instruction = '''
                        You are an expert blog content writer.Use Markdown formatting. 
                        Generate a blog title for the {topic}.
                        The title should be creative and SEO friendly'''
                
                prompt = ChatPromptTemplate.from_template(template = instruction)
                title_chain = prompt|self.llm

                response = title_chain.invoke({"topic":state["topic"]})

                return {"blog":{"title":response.content}}
        except Exception as e:
               raise CustomException(e,sys) from e    
        
    def content_generation(self,state:BlogState):

        try:

            if "topic" in state and state["topic"]:
                logging.info("Entering intocontent_generation node")

                system_prompt ="""
                            You are asn expert blog wrtiter. Use Markdown formatting.
                            Generate the detailed blog content with detailed breakdown for the topic {topic}"""
                
                prompt = ChatPromptTemplate.from_template(template = system_prompt)
                content_chain = prompt|self.llm

                response = content_chain.invoke({"topic":state["topic"]})

                return {"blog":{"content":response.content}}
        except Exception as e:
               raise CustomException(e,sys) from e
            
    def translation(self,state:BlogState):
        '''
        Translate the content to the specified language
        '''    
        try:
            translation_instruction = """
                    You are a professional translator.

                    Translate this blog into {current_language}.

                    Return ONLY a valid Blog object.

                    Rules:
                    - Do not add explanations
                    - Do not add markdown outside the fields
                    - Keep exactly two keys:
                    title
                    content

                    BLOG:
                    {blog_content}
                    """

            blog_content = state["blog"]["content"]
            prompt = ChatPromptTemplate.from_template(template = translation_instruction)
    
            structure_llm = self.llm.with_structured_output(Blog, method="function_calling")

            translational_chain = prompt|structure_llm

            response = translational_chain.invoke({"current_language":state["current_language"],"blog_content":blog_content})
            return {
            "blog": response.model_dump()
              }
        except Exception as e:
            raise CustomException(e,sys) from e



    def route(self,state:BlogState):
            try:
                return {"current_language":state["current_language"]}
            except Exception as e:
                raise CustomException(e,sys) from e

    def route_decision(self,state:BlogState):
         '''
         Route the content to the respective translation function
         '''   
         try:

            if state['current_language']=="hindi":
                return "hindi"
            
            if state["current_language"]=="french":
                return "french"
            
            else:
                return state["current_language"]
         except Exception as e:
            raise CustomException(e,sys) from e   