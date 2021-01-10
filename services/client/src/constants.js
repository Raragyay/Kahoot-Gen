import {
    red,
    volcano,
    orange,
    gold,
    yellow,
    lime,
    green,
    cyan,
    blue,
    geekblue,
    purple,
    magenta
} from '@ant-design/colors'

export const colors = {
    red: "#66101f",
    lightRed: "#855a5c",
    grey: "#8a8e91",
    blue: "#b8d4e3",
    green: "#eeffdb"
}
const tempColorArray = [red,
    volcano,
    orange,
    gold,
    yellow,
    lime,
    green,
    cyan,
    blue,
    geekblue,
    purple,
    magenta].map(arr => arr.slice(6, 10))

export const colorArray = [0, 1, 2, 3].map(i => tempColorArray.map(arr => arr[i]))
    .flat()