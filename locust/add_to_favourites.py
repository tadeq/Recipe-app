from locust import HttpLocust, TaskSet, task
from itertools import count

counter = count()
result_ids = ['b79327d05b8e5b838ad6cfd9576b30b6', '8275bb28647abcedef0baaf2dcf34f8b',
              '584ac5e486c088b3c8409c252d7f290c', '2463f2482609d7a471dbbf3b268bd956',
              'd81795fb677ba4f12ab1a104e10aac98', '4caf01683bf99ddc7c08c35774aae54c',
              '1817e7fccea9ae39d09c0e2c7fb86cb2', 'b7ad27e3e2c9440baca6ac8f7fac2a53',
              '0b1162a867624c9b60fc48ae880e848d', '690c3797b4f56fc1e119c14096d651c5',
              'b550f7f1182bc4d97f5473bcf15cf006', '71ab1bfee5b89e904185ef03c337d52b',
              'a252647971a0e2a8b3d1d7ee82191770', '7879614ad1d3687818ba7a494ef0bab9',
              '12fafbb01eadad8203145452e7ddc885', '9b6f45c3bcb793ba4663ee4c712d7759',
              'b4dadfbd094da0086d5759f92e9db359', '29560d04ec3094654c7d3977964a88f8',
              '3a8d2b01720fd964579c2eb2da2ff7cc', '4c86d901b3b5a57360aef1df63778217',
              'd9aa663c6adeaf1afb4296ed079694b3', '10abfbc20e802c832453500bcc50e1bd',
              'be3ba087e212f13672b553ecfa876333', 'af5b1e84bbd642d5759b51ba7d8e0389',
              '247d0bab750699d17787cbd9d5e30a6e', '82b35fb450ccafa9efa9eb7843632611',
              'a5f5ebf4cda1ebd61de3b92fce7082e3', '15a87fab966b3cb8a64ca118c690e55d',
              '9ca0499f2ac7f1e4cae63bdf4671c1b3', '639f2adeeb466e34af52e55cd807dfdf',
              '6901f5d7096ee93d044fa78080fc6445', '0902fe47921432fcb9b4ced4519686be',
              '63f409a7fbec68dbd88e6240c85d81b4', '6dd24204ea60cc37fe00bc2c691ab12e',
              '1c50ace4a9bce8145fc48e7b9188669e', '06ef542ad97f09eb9e5e71282d518574',
              'e94eb76b0a1ce22c3af7592a3a53a7c9', 'c26523951f822be0c9c49e1e0c59eda5',
              '1c8580c0aa7e3d57deea36ec96a2a66b', '10975d81f34a05f521c2f263c19132a0',
              'f8dccc0bc96add865b7790f2a18d5447', '95fa6f5689286a4ffab774da45192494',
              'd3ba35c87f5ab7946e3d7076cd51382e', '460a72418bb8eba10c59769b0751dc2b',
              'cb13a9986c54e96e4a4a1724bf33723b', 'f3b620c96a1486daf5d271549e9930e6',
              'af2b255ad6071c957008a4ccd5607489', 'c12146c6e13a25baf9a3cf77322bc732',
              '182eb4e5d92618a9e132d55cc9a080e5', 'fb0fe60fe06cb9737859f6452ce514f5',
              '1df9ec80efdc556d9e2b5c28cb08bc2f', '9c2a5ca55d1ec76cfeca208ab19db0f5',
              'e849a9bc5c41ce6238cc46448642eccf', '5ab36d4181b4f838057a0b46ac7df041',
              '55d79fe7d42285dbf6943ce32443dca6', 'd65e6cb0bf39fb5e92357ed6ad8f6d5a',
              'c816cbec14718f5b9ea79f42a7a0ea12', '26572a39d15d14fc887f67811cf443f9',
              '144c2ac67ff554bde40a81a972f93860', 'a4c35854fb493879d630506eaf488b1f',
              '4297d49fb5b534a861e4f267d3494726', 'b8af944c52674f962ad4b9743b99423a',
              '6b3186174d4f1102605a7ad132f95cf8', '33c6c39027b1812dc66dee916cdbbe27',
              '80ed0cee1342ebaa589d5298d758a99b', 'fdd0b2beb7f23866e371f73cab64526b',
              '1ad39d7b092cc9cdd5df330b36a45ecb', '053ec1218305383354a3d738554c8210',
              '0b5c2a177766eba8714bfa33eecebddd', 'f1eb630732258d9ed36cf67273e7ba47',
              '0fba4247b33344979546c83c281d0e65', 'd3e1cfef4b8fb3fe0ba6093d252d2b9b',
              '98ff4a6785985929f79b3cd26f762c3a', '0d01e97a5dd65112b37a3768c3fc8ae3',
              '13955de15ff1e8579a2dd484b1cfb491', 'ffba9f06808d023a7bc2b21ee6b54288',
              '89d5087668562fbffdcad52a17107bdf', 'afea16a3b9abd202693c9b17161cc489',
              '3b43078939cc1d88e718c6187fea32f8', '8ab853490e880044cab4c02fb1cbb8aa',
              '99f0dad15453226ce51c64785ba7aa2c', '6ed8f1773a6e2c01520958201e75eb83',
              '34fb4721184092b9ebcb51cd943796d1', '888e9fc4a808e9e4ccdb2ac24a6a2f46',
              '09d39ea731ede61f3cf163e0c56eaa44', '3b7cb2359876b5b27920156479e3286f',
              'a25ab6e41f439e4cc0721f3f34780da9', '3df870d810ca74099d44116e3cbe6745',
              'd9eb85d6e61a0ad7e7040398041681e6', '44ae882439011b9411dbca5f49fb1a36',
              '21c094917e4386fde6e4ad115e3d4a87', '96bb63a618e1a166d1566497fc6a3b01',
              '810491809765b4854019e9702ee8eadf', '4037aac585d67cea43bbdd174c8c5b9d',
              'ad9e782e7a0db340cf9427988c0c7c1c', 'ca0aca2408e7c34e422dd02edf4a2253',
              'f6e20da23282e0a4cfd08a572defefbb', 'a798c432f454674f165d4a52e4fd83b4',
              'ff978220ea227bbeb049b8fb081d84cd', 'f4ca562377dc9611ceb90cd056922243']


class WebsiteTasks(TaskSet):
    # query 'chicken' before

    @task(100)
    def delete_product(self):
        self.client.post('/recipes/' + result_ids[next(counter)])


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 0
    max_wait = 10000
