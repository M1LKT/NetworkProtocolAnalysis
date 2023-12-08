<template>
    <body>
        <div style="display: flex;width: 1050px;margin: auto;">
            <div style="flex:0.35;">
                <el-form :model="Settings" ref="Settings" :rules="rules" > 
                    <el-form-item prop="Counts" label="抓取数量">
                        <el-input v-model.number="Settings.Counts" placeholder="请输入抓取的流量包数量，默认为5条" ></el-input>
                    </el-form-item>
                </el-form>
            </div>
            <div style="flex:0.5;">
                <el-form :model="Settings" ref="Settings">
                    <el-form-item prop="Filter" label="过滤规则 src host 169.254.126.132">
                        <el-input v-model="Settings.Filter" placeholder="BPF过滤规则" clearable></el-input>
                    </el-form-item>
                </el-form>
            </div>
            <div style="flex:0.3;">
                <el-form :model="Settings" ref="Settings" > 
                    <el-form-item prop="Adapter" label="网卡（请选择正确可用的网卡设备）">
                        <el-select v-model="Settings.Adapter" clearable placeholder="请选择" style="width: 360px;">
                            <el-option
                            v-for="item in NetworkAdapters"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                </el-form>
            </div>
        </div>
        <el-card style="width: 1050px;margin: 0px auto;">
            <el-table :data="FlowPacket" style="width: 1000px;margin: 0px auto;border: 1px solid rgb(0, 0, 0);" height="290">
            <el-table-column label="概要" prop="summary"></el-table-column>
            </el-table>
        </el-card>
        <el-button type="primary" style="background:#505458 ;border:none ;margin-top: 40px;" @click="FlowCatch('Settings')">抓取</el-button>
        <el-button type="primary" style="background:#505458 ;border:none ;margin-top: 40px;" @click="SendJson('Settings')">发送json测试</el-button>
    </body>
</template>

<script>
export default{
    name:'Main',
    data(){
        return{
            FlowPacket:[],
            value:'',
            NetworkAdapters:[],
            Settings:{
                Counts:'',
                Adapter:'',
                Filter:''
            },
            rules: {
                Counts:[
                    {type: 'number', message: '必须为数字值'},
                ],
            },
        }
    },
    methods:{
        FlowCatch(formName){
            this.$refs[formName].validate((valid)=>{
                if(valid){
                    this.$request.post('/',this.Settings).then(res=>{
                        if(res.code=='200'){
                            this.FlowPacket=res.data
                            this.$message({
                            message: res.msg,
                            type: 'success',
                        });
                        console.log(this.Settings);
                        }
                    })
                }
            })
        },
        SendJson(formName){
            this.$refs[formName].validate((valid)=>{
                if(valid){
                    this.$request.post('/SendJson',this.Settings).then(res=>{
                        if(res.code=='200'){
                            this.FlowPacket=res.data
                            this.$message({
                            message: res.msg,
                            type: 'success',
                        });
                        console.log(this.Settings);
                        }
                    })
                }
            })
        }  
    },
   mounted(){
        this.$request.get('/SearchNIC').then(res=>{
            if(res.code=='200'){
                this.NetworkAdapters=res.data
            }
        })
   }
}
</script>