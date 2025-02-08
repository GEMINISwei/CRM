// Global
interface DataObject {
  [key: string]: any
}
interface OptionObject {
  text: string,
  value: any
}

// User Info
interface UserInfo {
  username: string
  token: string
  level: number,
  shift?: string
  idleTime?: number,
}

// CustomForm
interface CustomInputProps {
  label?: string
  type: string
  required?: boolean
  disabled?: boolean
  hidden?: boolean
  textPos?: string
}
interface CustomSearchListProps {
  label?: string
  required?: boolean
  disabled?: boolean
  hidden?: boolean
  textPos?: string
  options?: OptionObject[]
}
interface CustomSelectProps {
  label?: string
  required?: boolean
  disabled?: boolean
  hidden?: boolean
  textPos?: string
  options?: OptionObject[]
}
interface CustomTextareaProps {
  label?: string
  required?: boolean
  disabled?: boolean
  hidden?: boolean
  textPos?: string
  rows?: number
}
interface CustomFormField extends CustomInputProps, CustomSearchListProps, CustomSelectProps, CustomTextareaProps {
  step?: number
  depValue: string
  description?: string
}
interface CustomFormButton {
  step?: number
  color: string
  text: string
  method: Function
  needValid?: boolean
}

// DataTable
interface DataTableField {
  label: string
  depValue: string
  width: string
  canSearch?: boolean
}

// DataCard
interface DataCardField {
  label: string
  depValue: string
  canSearch?: boolean
}

interface FuncListItem {
  icon: string
  text: string
  method?: Function
  goPath?: string
}

export {
  DataObject,
  OptionObject,
  UserInfo,
  CustomInputProps,
  CustomSearchListProps,
  CustomSelectProps,
  CustomTextareaProps,
  CustomFormField,
  CustomFormButton,
  DataTableField,
  DataCardField,
  FuncListItem,
}
