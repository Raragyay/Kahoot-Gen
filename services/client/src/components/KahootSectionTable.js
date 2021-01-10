import React, {useState, useEffect} from 'react';
import {Button, Col, Input, Popconfirm, Space, Table} from 'antd';
import KahootQuestionTable from "./KahootQuestionTable";
import {PlusCircleOutlined, MinusCircleOutlined, CloseCircleOutlined, DownloadOutlined} from '@ant-design/icons'
import '../styles/App.less'
import {colorArray, colors} from '../constants'

function KahootSectionTable() {
    const [loading, setLoading] = useState(true)
    const [tableData, setTableData] = useState([])
    const [categories, setCategories] = useState({})
    const [questionTypes, setQuestionTypes] = useState({})
    const [questionTypesReversed, setQuestionTypesReversed] = useState({})
    const [downloadLoading, setDownloadLoading] = useState(false)
    const [excelLink, setExcelLink] = useState(null)

    useEffect(
        () => {
            fetch("/api/default-table")
                .then(response => {
                    if (!response.ok) {
                        throw Error(response.statusText)
                    } else {
                        return response.json()
                    }
                })
                .then(data => {
                    setTableData(data['tableData'])
                    setCategories(Object.fromEntries(data['categories'].map((category, idx) => [category, colorArray[idx]])))
                    setQuestionTypes(data['questionTypes'])
                    setQuestionTypesReversed(Object.fromEntries(Object.entries(data['questionTypes']).map(([k, v]) => [v, k])))
                }).then(() => {
                setLoading(false)
            })
        }, [] // run once
    )

    const onQuestionParamChange = sectionKey => param => questionKey => newCategories => {
        const tableDataCopy = [...tableData]
        const sectionIndex = tableDataCopy.findIndex(({key}) => key === sectionKey)
        const questionIndex = tableDataCopy[sectionIndex].questionGenerators.findIndex(({key}) => key === questionKey)
        Object.assign(tableDataCopy[sectionIndex].questionGenerators[questionIndex], {[param]: newCategories})
        setTableData(tableDataCopy)
    }

    const onQuestionCreate = sectionKey => () => {
        const tableDataCopy = [...tableData]
        const sectionIndex = tableDataCopy.findIndex(({key}) => key === sectionKey)
        const nextKey = tableData[sectionIndex].questionGenerators.length === 0 ? 0 :
            Math.max(...tableData[sectionIndex].questionGenerators.map(({key}) => key)) + 1
        const questionGeneratorsCopy = [...tableDataCopy[sectionIndex].questionGenerators] // Make copy of question generator array to force child component rerendering
        questionGeneratorsCopy.push({
            key: nextKey,
            questionType: '',
            categories: [],
            numOfQuestions: 0
        })
        Object.assign(tableDataCopy[sectionIndex], {questionGenerators: questionGeneratorsCopy})
        setTableData(tableDataCopy)
        onQuestionNumChange(sectionKey)() // this ensures that the updated question generator is in place for the new render
    }

    const onQuestionDelete = sectionKey => questionKey => () => {
        const tableDataCopy = [...tableData]
        const sectionIndex = tableDataCopy.findIndex(({key}) => key === sectionKey)
        const questionGeneratorsCopy = [...tableDataCopy[sectionIndex].questionGenerators].filter(({key}) => key !== questionKey) // Make copy of question generator array to force child component rerendering
        Object.assign(tableDataCopy[sectionIndex], {questionGenerators: questionGeneratorsCopy})
        setTableData(tableDataCopy)
        onQuestionNumChange(sectionKey)()
    }

    const onQuestionNumChange = sectionKey => () => {
        const tableDataCopy = [...tableData]
        const sectionIndex = tableDataCopy.findIndex(({key}) => key === sectionKey)
        const numOfQuestions = tableDataCopy[sectionIndex].questionGenerators.map(({numOfQuestions}) => numOfQuestions).reduce((x, y) => x + y, 0)
        Object.assign(tableDataCopy[sectionIndex], {numOfQuestions: numOfQuestions})
        setTableData(tableDataCopy)
    }

    const onSectionCreate = () => {
        const tableDataCopy = [...tableData]
        const nextKey = tableDataCopy.length === 0 ? 0 : Math.max(...tableDataCopy.map(({key}) => key)) + 1
        tableDataCopy.push({
            key: nextKey,
            sectionPrompt: '',
            numOfQuestions: 0,
            questionGenerators: []
        })
        setTableData(tableDataCopy)
    }

    const onSectionDelete = sectionKey => () => {
        const tableDataCopy = [...tableData]
        setTableData(tableDataCopy.filter(({key}) => key !== sectionKey))
    }

    const clearTable = () => {
        setTableData([])
    }

    const submitToAPIExcel = () => {
        setDownloadLoading(true)
        fetch("/api/excel", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'kahootData': tableData})
        }).then(response => response.json())
            .then(json => setExcelLink(json.fileId))
            .then(() => setDownloadLoading(false))
    }

    const fetchExcelLink = (fileId) => {
        fetch(`/api/excel/${fileId}`)
            .then(response => response.blob())
            .then(blob => URL.createObjectURL(blob))
            .then(url => {
                let a = document.createElement('a')
                a.style = 'display:none'
                document.body.append(a)
                a.href = url
                a.download = 'KahootGenQuiz.xlsx' // gives the file a name
                a.click()
                URL.revokeObjectURL(url)
            })
    }

// render
    return (
        <>
            <Table
                expandable={
                    {
                        expandedRowRender: ({questionGenerators, key}) =>
                            KahootQuestionTable(
                                questionGenerators,
                                categories,
                                questionTypes,
                                questionTypesReversed,
                                onQuestionParamChange(key),
                                onQuestionCreate(key),
                                onQuestionDelete(key),
                                onQuestionNumChange(key)
                            ),
                        expandIcon: ({expanded, onExpand, record}) => {
                            const params = {
                                onClick: e => onExpand(record, e),
                                // twoToneColor: colors.red
                            }
                            return expanded ?
                                (<MinusCircleOutlined {...params}/>) :
                                (<PlusCircleOutlined {...params}/>)
                        }
                    }
                }
                dataSource={tableData}
                loading={loading}
                pagination={{position: ['bottomRight']}}
                rowKey={({key}) => key}
                footer={(currentPageData) => {
                    return (
                        <Space
                            wrap={true}
                        >
                            <Button
                                onClick={onSectionCreate}
                                type='primary'
                            >
                                Add a section
                            </Button>
                            <Button
                                onClick={clearTable}
                                type={'primary'}
                            >
                                Reset Table
                            </Button>
                            <Button
                                onClick={submitToAPIExcel}
                                type={'primary'}
                            >
                                Create Excel file
                            </Button>
                            <Button
                                type={'primary'}
                                icon={<DownloadOutlined/>}
                                loading={downloadLoading}
                                disabled={excelLink === null}
                                onClick={() => fetchExcelLink(excelLink)}
                            >
                                Download
                            </Button>
                        </Space>
                    )
                }}
                    >
                    <Col
                    title='# of Questions'
                    dataIndex='numOfQuestions'
                    key='numOfQuestions'
                    width='10%'
                    />
                    <Col
                    title='Section Prompt'
                    dataIndex='sectionPrompt'
                    key='sectionPrompt'
                    width='90%'
                    render={(text, record) => {
                    const params = {
                    defaultValue: text,
                    key: record.key,
                    maxLength: 120, //Kahoot given
                    onChange: e => {
                    const tableDataCopy = [...tableData]
                    const editedItemIndex = tableDataCopy.findIndex(({key}) => key === record.key)
                    Object.assign(tableDataCopy[editedItemIndex], {'sectionPrompt': e.target.value})
                    setTableData(tableDataCopy)
                },
                    placeholder: 'Enter a prompt for this section!'
                }
                    return <Input {...params}/>
                }}
                    />
                    <Col
                    title=''
                    key='deleteAction'
                    render={(_, {key}) =>
                    <Popconfirm
                    title='Are you SURE you want to delete this section?'
                    onConfirm={onSectionDelete(key)}
                    placement={'rightBottom'}
                    >
                    <CloseCircleOutlined
                    twoToneColor={colors.red}
                    />
                    </Popconfirm>
                }
                    />
                    </Table>
                    </>
                    )
                }

export default KahootSectionTable