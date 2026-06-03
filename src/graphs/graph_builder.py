from langgraph.graph import StateGraph,END,START
from src.llms.groqllm import GroqLLM
from src.state.blogstate import BlogState
from src.nodes.blog_node import BlogNode

class GraphBuilder:
    def __init__(self,llm):
        self.llm = llm
        self.graph_builder = StateGraph(BlogState)
        self.blog_node = BlogNode(self.llm)

    def build_topic_graph(self):
        '''
        Build a graph to generate blogs based on topic'''    

        # Nodes
        self.graph_builder.add_node("title_creation",self.blog_node.title_creation)
        self.graph_builder.add_node("content_generation",self.blog_node.content_generation)

        #Edges
        self.graph_builder.add_edge(START,"title_creation")
        self.graph_builder.add_edge("title_creation","content_generation")
        self.graph_builder.add_edge("content_generation",END)

        return self.graph_builder
    
    def build_language_graph(self):
        '''
        Building a graph for blog generation with inputs topics and language
        '''
        # Nodes
        self.graph_builder.add_node("title_creation",self.blog_node.title_creation)
        self.graph_builder.add_node("content_generation",self.blog_node.content_generation)
        self.graph_builder.add_node("hindi_translation",lambda state:self.blog_node.translation({**state,"current_language":"hindi"}))
        self.graph_builder.add_node("french_translation",lambda state:self.blog_node.translation({**state,"current_language":"french"}))
        self.graph_builder.add_node("route",self.blog_node.route)

        ##  Building Edges
        self.graph_builder.add_edge(START,"title_creation")
        self.graph_builder.add_edge("title_creation","content_generation")
        self.graph_builder.add_edge("content_generation","route")
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




    def setup_graph(self,usecase):
        if usecase=="topic":
            self.build_topic_graph()

        if usecase=="language":
            self.build_language_graph()

        return self.graph_builder.compile() 


# below code for langsmith langgraph studio
llm = GroqLLM().get_llm_model()

##get the graph
graph_builder= GraphBuilder(llm)
graph = graph_builder.build_language_graph().compile()
