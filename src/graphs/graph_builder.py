from langgraph.graph import StateGraph,END,START
from src.llms.groqllm import GroqLLM
from src.state.blogstate import BlogState
from src.nodes.blog_node import BlogNode
from src.exception import CustomException
from src.logger import logging
import sys

class GraphBuilder:
    def __init__(self,llm):
        self.llm = llm
        self.graph_builder = StateGraph(BlogState)
        self.blog_node = BlogNode(self.llm)

    def build_topic_graph(self):
        '''
        Build a graph to generate blogs based on topic'''    
        try:
            # Nodes
            self.graph_builder.add_node("title_creation",self.blog_node.title_creation)
            self.graph_builder.add_node("content_generation",self.blog_node.content_generation)

            #Edges
            self.graph_builder.add_edge(START,"title_creation")
            self.graph_builder.add_edge("title_creation","content_generation")
            self.graph_builder.add_edge("content_generation",END)

            return self.graph_builder
        except Exception as e:
            raise CustomException(e,sys) from e
        

    def build_language_graph(self):
        '''
        Building a graph for blog generation with inputs topics and language
        '''
        try:

            logging.info("starting building graph nodes for language")

            # Nodes
            self.graph_builder.add_node("title_creation",self.blog_node.title_creation)
            self.graph_builder.add_node("content_generation",self.blog_node.content_generation)
            self.graph_builder.add_node("hindi_translation",lambda state:self.blog_node.translation({**state,"current_language":"hindi"}))
            self.graph_builder.add_node("french_translation",lambda state:self.blog_node.translation({**state,"current_language":"french"}))
            self.graph_builder.add_node("route",self.blog_node.route)

            ##  Building Edges
            logging.info("starting building graph edgesfor language")


            self.graph_builder.add_edge(START,"title_creation")
            self.graph_builder.add_edge("title_creation","content_generation")
            self.graph_builder.add_edge("content_generation","route")

            logging.info("Entering into routing")

            self.graph_builder.add_conditional_edges(
                "route",
                self.blog_node.route_decision,
                {
                    "hindi":"hindi_translation",
                    "french":"french_translation"
                }
                
            )
            self.graph_builder.add_edge("hindi_translation",END)
            self.graph_builder.add_edge("french_translation",END)

            return self.graph_builder
        except Exception as e:
                raise CustomException(e,sys) from e



    def setup_graph(self,usecase):
        try:
            if usecase=="topic":
                logging.info("starting building graph for only topic")

                self.build_topic_graph()

            if usecase=="language":
                logging.info("starting building graph for  topic and language")
                self.build_language_graph()

            return self.graph_builder.compile()
        except Exception as e:
            raise CustomException(e,sys) from e
 


# below code for langsmith langgraph studio
llm = GroqLLM().get_llm_model()

##get the graph
graph_builder= GraphBuilder(llm)
graph = graph_builder.build_language_graph().compile()
