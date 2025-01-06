import axios from 'axios'

// 创建axios实例
const request = axios.create({
    baseURL: 'http://127.0.0.1:5000',
    timeout: 5000,
})


export default request