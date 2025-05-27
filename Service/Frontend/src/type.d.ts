// Global
interface DataObject {
  [key: string]: any
}
interface FormFields {
  [key: string]: DataObject
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
  max?: number
  min?: number
}
interface CustomSearchListProps {
  label?: string
  type: string
  required?: boolean
  disabled?: boolean
  hidden?: boolean
  textPos?: string
  options?: OptionObject[]
}
interface CustomSelectProps {
  label?: string
  type: string
  required?: boolean
  disabled?: boolean
  hidden?: boolean
  textPos?: string
  options?: OptionObject[]
}
interface CustomTextareaProps {
  label?: string
  type: string
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


// BaseForm
interface BaseFormButton {
  color: string
  text: string
  method: Function
  hidden?: boolean
  needValid?: boolean
}
interface BaseFormProps {
  columnGap?: number
  colSize?: number
  colOffset?: number
  textPos?: string
  btnPos?: string
}
interface BaseFormNumber {
  max?: number
  min?: number
}
interface BaseFormTextarea {
  rows?: number
}
interface BaseFormSelect {
  options?: []
}
interface BaseFormField extends BaseFormNumber, BaseFormTextarea, BaseFormSelect {
  type: string
  label?: string
  required?: boolean
  disabled?: boolean
  hidden?: boolean
  description?: string
}
interface BaseFormFields {
  [key: string]: BaseFormField
}


export {
  DataObject,
  FormFields,
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

  // BaseForm
  BaseFormButton,
  BaseFormProps,
  BaseFormField,
  BaseFormFields
}
