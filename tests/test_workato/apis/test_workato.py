from tests.test_workato.common.utils import compare_dict_keys

def test_managed_user(workato, mock_workato):
    """
    Test Workato Connections API
    
    Parameters:
        workato (obj): Workato Instance
        mock_workato (obj): mock workato instance
    """

    managed_user = workato.managed_users.get()['result']
    mock_managed_user = mock_workato.managed_users.get_all()

    assert compare_dict_keys(managed_user[0], mock_managed_user) == set()
    assert compare_dict_keys(mock_managed_user, managed_user[0]) == set()

def test_connections(workato, mock_workato):
    """
    Test Workato Connections API
    
    Parameters:
        workato (obj): Workato Instance
        mock_workato (obj): mock workato instance
    """
    
    connections = workato.connections.get(890744)['result']
    mock_connections = mock_workato.connections.get_all()
    
    assert compare_dict_keys(connections[0], mock_connections) == set()
    assert compare_dict_keys(mock_connections, connections[0]) == set()
    
def test_folders(workato, mock_workato):
    """
    Test Workato Connections API
    
    Parameters:
        workato (obj): Workato Instance
        mock_workato (obj): mock workato instance
    """
    
    folders = workato.folders.get(890744)['result']
    mock_folders = mock_workato.folders.get_all()
    
    assert compare_dict_keys(folders[0], mock_folders) == set()
    assert compare_dict_keys(mock_folders, folders[0]) == set()
    
    
def test_recipes(workato, mock_workato):
    """
    Test Workato Connections API
    
    Parameters:
        workato (obj): Workato Instance
        mock_workato (obj): mock workato instance
    """

    recipes = workato.recipes.get(890744)['result']
    mock_recipes = mock_workato.recipes.get_all()
    
    assert compare_dict_keys(recipes[0], mock_recipes) == set()
    assert compare_dict_keys(mock_recipes, recipes[0]) == set()
