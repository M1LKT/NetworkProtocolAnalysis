import router from '@/router';
import axios from 'axios'

//创建一个新的axios对象
const request =axios.create({
    baseURL:'http://localhost:5000',
    timeout:300000
})
//request拦截器
//发送前对请求进行处理，如统一添加token
request.interceptors.request.use(config => {
    config.headers['Content-Type'] = 'application/json;charset=UTF-8';
    // let user=JSON.parse(localStorage.getItem("user") || '{}') //将存储进localstorage的数据取出并且解析成json，如果没有数据解析则返回空("{}")
    // config.headers['token']=user.token
    return config
},error=>{
    console.error('request error: '+error)
    return Promise.reject(error) //打印错误
})

//4.2 添加响应拦截器
request.interceptors.response.use(response => {
    let res=response.data;
    //兼容返回的字符串数据
    if (typeof res ==="string"){
        res= res ? JSON.parse(res) :res
    }
    if(res.code==='401'){
        router.push('/')
    }
    return res;
},error=>{
    console.error('response error: '+error)
    return Promise.reject(error) //打印错误
})

export default request; 