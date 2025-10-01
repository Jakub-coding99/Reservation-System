clients = [{"client" : 1},{"client" : 2},{"client" : 3},]

def test():
    for client in clients:
        if client["client"] == 1:
            continue
        else:
            print(client)
       
test()