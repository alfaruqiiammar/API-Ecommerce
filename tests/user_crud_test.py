import json
from . import app, user, cache, create_token_admin, create_token_user


class TestUserCrud():
    var = 0

    def test_User_valid_input_post_name(self, user):
        token = create_token_admin()
        data = {
            'username': 'coba222',
            'email': 'cobaemai222',
            'password': 'satudua1',
            'status': True,
        }
        # karena post menggunakan data, sedangkan get menggunkan query_string
        res = user.post('/user', data=json.dumps(data),
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')

        res_json = json.loads(res.data)
        TestUserCrud.var = res_json['user_id']
        assert res.status_code == 200

    def test_User_invalid_post_name(self, user):
        token = create_token_admin()
        data = {
            'username': 'ammar',
            'status': True,
        }
        # karena post menggunakan data, sedangkan get menggunkan query_string
        res = user.post('/user', data=json.dumps(data),
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_user_getlist(self, user):  # user dr init test
        token = create_token_admin()
        res = user.get('/user',
                       headers={'Authorization': 'Bearer ' + token},
                       content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_invalid_user_getlist(self, user):  # user dr init test
        token = create_token_admin()
        res = user.get('/daftar/list112',
                       headers={'Authorization': 'Bearer ' + token},
                       content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_user_get_valid_id_token(self, user):
        token = create_token_user()
        res = user.get('/user/'+str(TestUserCrud.var),
                       headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_get_invalid_id_token(self, user):
        res = user.get('/user/25',
                       headers={'Authorization': 'Bearer abc'})

        res_json = json.loads(res.data)
        assert res.status_code == 500

    def test_user_valid_put_token(self, user):
        token = create_token_admin()
        data = {
            'username': 'ganti11',
            'email': 'gantiemail111',
            'password': 'satudua11',
            'status': True,
        }
        res = user.put('/user/'+str(TestUserCrud.var),
                       headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_user_invalid_put_token(self, user):
        token = create_token_admin()
        data = {
            'username': 'SECRET10',
        }
        res = user.put('/user/15',
                       headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_user_valid_delete_token(self, user):
        token = create_token_admin()
        res = user.delete('/user/'+str(TestUserCrud.var),
                          headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_invalid_delete_token(self, user):
        token = create_token_admin()
        res = user.delete('/user/120',
                          headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 404
