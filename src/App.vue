<template>
  <el-container>
    <el-main>
      <h1>
        Permanent Posting Based On Arweave Network
      </h1>
      <el-row>
        <el-col :span="12">
          <el-row>
            <el-input v-model="key" :rows="5" type="textarea" placeholder="key"/>
          </el-row>
          <el-row>
            <el-input v-model="send_data" :rows="15" type="textarea" placeholder="post data"/>
          </el-row>
          <el-row>
            <el-input v-model="send_id" placeholder="post id"/>
          </el-row>
          <el-row>
            <el-button type="primary" @click="postData">Post</el-button>
          </el-row>
        </el-col>
        <el-col :span="12">
            <el-row>
              <el-input v-model="recv_id" :rows="2" type="textarea" placeholder="post id"/>
            </el-row>
            <el-row>
              <el-input v-model="recv_data" :rows="15" type="textarea" placeholder="post data"/>
            </el-row>
            <el-row>
              <el-button type="primary" @click="getData">Get</el-button>
            </el-row>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<style scoped>
.el-row {
  margin: 20px;
}
</style>

<script>
import Arweave from 'arweave';

export default {
  data() {
    return {
      send_id: "",
      recv_id: "",
      key: "",
      send_data: "",
      recv_data: "",
      arweave: Arweave.init({}),
    }
  },
  methods: {
    postData() {
      this.uploading(this.key, this.send_data);
    },
    getData() {
      this.downloading(this.recv_id);
    },
    getInfo() {
      arweave.network.getInfo().then(console.log);
    },
    async uploading(key, data) {
      key = JSON.parse(key);
      let transaction = await this.arweave.createTransaction({ data:data }, key);
      console.log(transaction);
      await this.arweave.transactions.sign(transaction, key);
      let uploader = await this.arweave.transactions.getUploader(transaction);
      while (!uploader.isComplete) {
        await uploader.uploadChunk();
        console.log(`${uploader.pctComplete}% complete, ${uploader.uploadedChunks}/${uploader.totalChunks}`);
      }
      this.send_id = transaction.id;
    },
    async downloading(id) {
      this.arweave.transactions.getData(this.recv_id).then(data => {this.recv_data = window.atob(data)});
    }
  }
}
</script>