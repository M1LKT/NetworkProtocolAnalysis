<template>
    <div>
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
        <div>
            <h2>{{ AnalysisResult }}</h2>
            <img v-if="Image1Name" :src="this.$request.defaults.baseURL+'/get_image/' + Image1Name" alt="My Image">
        </div>
    </div>
</template>

<script>
  export default {
    data() {
      return {
        fileList: [],
        AnalysisResult: '',
        Image1Name:''
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
                this.AnalysisResult=response.data.AnalysisResult
                console.log(response.data[1].Image1.imageName)
                this.Image1Name=response.data[1].Image1.imageName
            }
            console.log(response);  // 这里可以处理你的响应
        },
    },
    // mounted(){
    //         console.log('1')
    //         console.log(this.$request.defaults.baseURL)
    // }
  }
</script>