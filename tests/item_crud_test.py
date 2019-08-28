import json
from . import app, user, cache, create_token_admin, create_token_user


class TestItemCrud():
    var = 0

    def test_Item_valid_input_post(self, user):
        token = create_token_admin()
        data = {
            'nama': 'testing3',
            'detail': 'testing3',
            'url': 'aaaaa',
            'harga': 2000,
            'total': 1,
        }
        # karena post menggunakan data, sedangkan get menggunkan query_string
        res = user.post('/item', data=json.dumps(data),
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')

        res_json = json.loads(res.data)
        TestItemCrud.var = res_json['item_id']
        assert res.status_code == 200

    def test_Item_invalid_post(self, user):
        token = create_token_admin()
        data = {
            'nama': 'gagal',
            'detail': "cobagagal",
        }
        # karena post menggunakan data, sedangkan get menggunkan query_string
        res = user.post('/user', data=json.dumps(data),
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_Item_getlist(self, user):  # user dr init test
        token = create_token_admin()
        res = user.get('/item',
                       headers={'Authorization': 'Bearer ' + token},
                       content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_invalid_item_getlist(self, user):  # user dr init test
        token = create_token_admin()
        res = user.get('/item/list112',
                       headers={'Authorization': 'Bearer ' + token},
                       content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_item_valid_put(self, user):
        token = create_token_admin()
        data = {
            'nama': 'ganti2',
            'detail': 'ganti2',
            'url': 'aaaaa',
            'harga': 2000,
            'total': 1,
        }
        res = user.put('/item/'+str(TestItemCrud.var),
                       headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_item_invalid_put(self, user):
        token = create_token_admin()
        data = {
            'nama': 'ganti2',
            'detail': 'ganti2',
            'url': 'aaaaa',
        }
        res = user.put('/item/15',
                       headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_user_valid_delete_token(self, user):
        token = create_token_admin()
        res = user.delete('/item/'+str(TestItemCrud.var),
                          headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_item_invalid_delete_token(self, user):
        token = create_token_admin()
        res = user.delete('/item/120',
                          headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 404
