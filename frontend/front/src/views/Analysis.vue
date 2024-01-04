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
        <div v-if="Imagename !== ''">
            <el-button type="text" @click="showAiAnalysis()">查看ai分析</el-button>
            <el-dialog
                title="内容来自于讯飞星火大模型，仅供参考"
                :visible.sync="dialogVisible"
                width="30%"
                :before-close="handleClose">
                <p v-if="fullText.length > 0" >{{ textToShow }}</p>
                <div v-else>
                    <p style="margin-bottom: 20px;">正在分析中，请稍后...</p>
                    <div class="loading">
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                    </div>
                </div>
                <span slot="footer" class="dialog-footer">
                    <el-button @click="refresh()">刷 新</el-button>
                    <el-button type="primary" @click="justClose()">确 定</el-button>
                </span>
            </el-dialog>
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
                ],
                dialogVisible: false,
                fullText: '',
                textToShow: '',
                intervalId: null,
            };
        },
        methods: {
            handleChange(file, fileList) {
                this.fileList = fileList.slice(-1);
                this.fullText = '';
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
                    this.Imagename = [];
                    this.AnalysisResult=response.data[0].AnalysisResult
                    console.log(response.data[1].Image1.imageName)
                    this.Imagename.push(response.data[1].Image1.imageName)
                    this.Imagename.push(response.data[2].Image2.imageName)
                    this.Imagename.push(response.data[3].Image3.imageName)
                    this.$request.post('/AIAnalysisFlow').then(res=>{
                        if(res.code=='200'){
                            this.fullText=res.data
                        }
                    })
                }
                console.log(response);  // 这里可以处理你的响应
            },
            handleClose(done) {
                this.$confirm('确认关闭？')
                .then(_ => {
                    clearInterval(this.intervalId);
                    this.textToShow = '';
                    done();
                })
                .catch(_ => {});
            },
            showAiAnalysis() {
                this.dialogVisible = true;
                this.startPrinting();
            },
            startPrinting() {
                let i = 0;
                this.intervalId = setInterval(() => {
                    if (i < this.fullText.length) {
                    this.textToShow += this.fullText[i];
                    i++;
                    } else {
                    clearInterval(this.intervalId);
                    }
                }, 50);
            },
            justClose() {
                this.dialogVisible = false;
                clearInterval(this.intervalId);
                this.textToShow = '';
            },
            refresh() {
                this.fullText = '';
                this.textToShow = '';
                this.$request.post('/AIAnalysisFlow').then(res=>{
                    if(res.code=='200'){
                            this.fullText=res.data
                        }
                })
            },
        },
        watch: {
                fullText(newValue) {
                    if (newValue.length > 0 && this.dialogVisible==true) {
                        this.startPrinting();
                    }
                },
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

<style lang="less">
@import '../style/load.less';

</style>