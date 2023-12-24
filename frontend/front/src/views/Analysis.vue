<template>
    <div style="width: 1000px;margin: 0px auto;">
        <el-upload
            drag
            class="upload-demo"
            action="http://localhost:5000//PcapFile"
            :on-change="handleChange"
            :on-success="handleSuccess"
            :file-list="fileList">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
            <div class="el-upload__tip" slot="tip">支持pcap、pcapng文件</div>
        </el-upload>
    </div>
</template>

<script>
  export default {
    data() {
      return {
        fileList: []
      };
    },
    methods: {
        handleChange(file, fileList) {
            this.fileList = fileList.slice(-1);
        },
        handleSuccess(response, file, fileList) {
            if (response.code !== "200") {
                this.$message({
                    message: response.msg,
                    type: 'error'
                });
            } else {
                this.$message({
                    message: response.msg,
                    type: 'success'
                });
            }
            console.log(response);  // 这里可以处理你的响应
        }
    }
  }
</script>