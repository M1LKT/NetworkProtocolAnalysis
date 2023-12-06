<template>
    <body>
        <h1>hello world!</h1>
        <el-card style="width: 1050px;margin: 0px auto;">
            <el-table :data="FlowPacket" style="width: 1000px;margin: 0px auto;border: 1px solid rgb(0, 0, 0);">
            <el-table-column label="Summary" prop="summary"></el-table-column>
            </el-table>
        </el-card>
        <el-button type="primary" style="background:#505458 ;border:none ;margin-top: 40px;" @click="FlowCatch()">抓取</el-button>
    </body>
</template>

<script>
export default{
    name:'main',
    data(){
        return{
            FlowPacket:[],
            testdata:[{
            "summary": "Ether / PPPoE / PPP / IP / TCP 111.13.116.110:https > 10.108.26.90:65421 PA / Raw"
        },
        {
            "summary": "Ether / PPPoE / PPP / IP / TCP 10.108.26.90:65421 > 111.13.116.110:https PA / Raw"
        },
        {
            "summary": "Ether / PPPoE / PPP / IP / TCP 111.13.116.110:https > 10.108.26.90:65421 A / Padding"
        },
        {
            "summary": "Ether / PPPoE / PPP / IP / UDP 10.108.26.90:58526 > 183.236.59.177:9999 / Raw"
        },
        {
            "summary": "Ether / PPPoE / PPP / IP / TCP 10.108.26.90:63801 > 20.189.173.15:https FA"
            }]
        }
    },
    methods:{
        FlowCatch(){
            this.$request.get('/').then(res=>{
                if(res.code=='200'){
                    this.FlowPacket=res.data
                    this.$message({
                    message: res.msg,
                    type: 'success',
                });
                }
            })
        }
    }
}
</script>