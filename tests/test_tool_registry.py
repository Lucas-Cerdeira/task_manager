def test_tool_registry(client):
    response = client.get("/tool-registry/")
    assert response.status_code == 200
    data = response.json()
    
    # Verifica se é uma lista
    assert isinstance(data, list)
    
    # Verifica se há ferramentas na lista
    assert len(data) > 0
    
    # Verifica a estrutura de cada ferramenta
    for tool in data:
        assert "name" in tool
        assert "description" in tool
        assert "url" in tool
        assert "method" in tool
        assert "schema" in tool
        assert "input" in tool["schema"]
        assert "output" in tool["schema"]
        
    # Verifica se as ferramentas principais estão presentes
    tool_names = [tool["name"] for tool in data]
    assert "create_task" in tool_names
    assert "get_task" in tool_names
    assert "update_task" in tool_names
    assert "delete_task" in tool_names
