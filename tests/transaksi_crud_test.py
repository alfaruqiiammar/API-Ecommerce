import json
from . import app, user, cache, create_token_admin, create_token_user


class TestTransCrud():
    var = 0

    def test_Trans_valid_input_post_name(self, user):
        token = create_token_admin()
        data = {
            'user_id': 2,
            'item_id': 1,
            'nama_item': 'testtingfix11',
            'total_qty': 10,
            'total_harga': 10,
            'tanggal': "Aug 28 2019",
        }
        # karena post menggunakan data, sedangkan get menggunkan query_string
        res = user.post('/transaksi', data=json.dumps(data),
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')

        res_json = json.loads(res.data)
        TestTransCrud.var = res_json['user_id']
        assert res.status_code == 200

    def test_transaksi_invalid_post_name(self, user):
        token = create_token_admin()
        data = {
            'user_id': 2,
            'item_id': 1,
            'nama_item': 'testting1',
            'total_qty': 10,
        }
        # karena post menggunakan data, sedangkan get menggunkan query_string
        res = user.post('/transaksi', data=json.dumps(data),
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_transaksi_getlist(self, user):  # user dr init test
        token = create_token_admin()
        res = user.get('/transaksi',
                       headers={'Authorization': 'Bearer ' + token},
                       content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_invalid_transaksi_getlist(self, user):  # user dr init test
        token = create_token_admin()
        res = user.get('/transaki/list112',
                       headers={'Authorization': 'Bearer ' + token},
                       content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_transaksi_valid_put_token(self, user):
        token = create_token_admin()
        data = {
            'user_id': 2,
            'item_id': 1,
            'nama_item': 'gantitesting1',
            'total_qty': 10,
            'total_harga': 10,
            'tanggal': "Aug 28 2019",
        }
        res = user.put('/transaki/'+str(TestTransCrud.var),
                       headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_transaksi_invalid_put_token(self, user):
        token = create_token_admin()
        data = {
            'user_id': 2,
            'item_id': 1,
            'nama_item': 'gantitesting1',
            'total_qty': 10,
        }
        res = user.put('/transaksi/2',
                       headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_transaksi_valid_delete_token(self, user):
        token = create_token_admin()
        res = user.delete('/transaksi/'+str(TestTransCrud.var),
                          headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 500

    def test_transaksi_invalid_delete_token(self, user):
        token = create_token_admin()
        res = user.delete('/transaki/120',
                          headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 404
