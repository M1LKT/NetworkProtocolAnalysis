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
        </div>
        <div v-if="Imagename !== ''" style="width: 800px;;margin: 0px auto;">
            <el-carousel type="card" height="350px" :autoplay="false" arrow="never">
                <el-carousel-item item v-for="(item,index) in Imagename" :key="item"  style="background-color: aliceblue;" >
                    <img :src="$request.defaults.baseURL+'/get_image/' + item" style="width: 100%; height: 300px;"  alt="Carousel Image">
                    <p style="width: 100%; height: auto;">{{ LabelName[index] }}</p>
                </el-carousel-item>
            </el-carousel>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
        return {
            fileList: [],
            AnalysisResult: '',
            Imagename:[],
            LabelName:[
                '业务流量占比',
                '业务流量通信主机数',
                '业务流量速率',
            ]
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
                    this.AnalysisResult=response.data[0].AnalysisResult
                    console.log(response.data[1].Image1.imageName)
                    this.Imagename.push(response.data[1].Image1.imageName)
                    this.Imagename.push(response.data[2].Image2.imageName)
                    this.Imagename.push(response.data[3].Image3.imageName)
                }
                console.log(response);  // 这里可以处理你的响应
            }
        },
    }
</script>

<style>
  .el-carousel__item h3 {
    color: #475669;
    font-size: 14px;
    opacity: 0.75;
    line-height: 200px;
    margin: 0;
  }
  
  .el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
  }
  
  .el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
  }
</style>