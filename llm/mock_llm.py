class MockLLM:
    def invoke(self, prompt):
        class Response:
            content = (
                "Mock response: Based on the sales data, "
                "the West region generated the highest revenue."
            )
        return Response()
