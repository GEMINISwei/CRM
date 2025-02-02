import axios from 'axios'
import type { DataObject } from '@/type'

const apiUrl = import.meta.env.VITE_API_URL

const callApi = (method: string, path: string, data?: DataObject) => {
  return new Promise((resolve, reject) => {
    let requestData: DataObject = {}

    if (data) {
      Object.keys(data).forEach((key: string) => {
        if (data[key] !== '') {
          requestData[key] = data[key]
        }
      })
    }

    axios({
      method: method,
      url: `${apiUrl + path}`,
      data: requestData,
    })
      .then((res: any) => {
        resolve(res.data)
      })
      .catch((err: any) => {
        console.log("status:", err.response.status)
        console.log("message:", err.response.data.detail)
        reject(err.response)
      })
  })
}

const callMultipleGetApi = (paths: string[]) => {
  return new Promise((resolve, reject) => {
    axios.all(paths.map((path: string) => axios.get(`${apiUrl + path}`)))
      .then((res: any) => {
        resolve(res.map((x: any) => x.data))
      })
      .catch((err: any) => {
        err.forEach((e: any) => {
          console.log("status:", e.response.status)
          console.log("message:", e.response.data.detail)
        })
        reject(err)
      })
  })
}

export {
  callApi,
  callMultipleGetApi
}
