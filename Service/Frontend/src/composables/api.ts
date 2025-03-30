import axios from 'axios'
import { setStatusFlag, currentUser, initUser } from '@/composables/globalUse'
import { goPage } from '@/router'
import { createNotify } from '@/composables/notify'
import type { DataObject } from '@/type'

const apiUrl = import.meta.env.VITE_API_URL

const callApi = (method: string, path: string, data?: DataObject, isBlob: boolean = false) => {
  return new Promise((resolve, reject) => {
    let axiosConfig: DataObject = {
      method: method,
      url: `${apiUrl + path}`,
      data: {},
    }

    if (currentUser.token) {
      axiosConfig["headers"] = {
        "Authorization": `Bearer ${currentUser.token}`,
      }
    }

    if (data) {
      Object.keys(data).forEach((key: string) => {
        if (data[key] !== '') {
          axiosConfig.data[key] = data[key]
        }
      })
    }

    if (isBlob) {
      axiosConfig["responseType"] = "blob"
    }

    axios(axiosConfig)
      .then((res: any) => {
        if (isBlob) {
          const blob = new Blob([res.data], { type: res.headers['content-type'] });

          resolve(blob)
        } else {
          resolve(res.data)
        }
      })
      .catch((err: any) => {
        console.log("status:", err.response.status)
        console.log("message:", err.response.data.detail)

        if (err.response.status == 401 &&
            err.response.data.detail == "Signature has expired") {
          callApi("post", "/apis/users/logout", {
            username: currentUser.username
          })
            .then((_) => {
              initUser()
              setStatusFlag("loading", false)
              goPage('/')
              createNotify("info", "憑證已過期, 請重新登入 !")
            })
            .catch((_) => {
              createNotify("error", "憑證處理異常 !")
            })
        }
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
