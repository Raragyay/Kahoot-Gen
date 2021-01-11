import React from 'react';
import {Table, Col, Tag, Select, InputNumber, Button, Tooltip, Space, Typography, List} from 'antd';
import {CloseCircleOutlined, WarningOutlined} from "@ant-design/icons";
import {colors} from "../constants";
import {sumBy, pick} from 'lodash'

export default function KahootQuestionTable(questionGenerators,
                                            categoryToData,
                                            questionTypes,
                                            questionTypesReversed,
                                            onParamChange,
                                            onQuestionCreated,
                                            onQuestionDeleted,
                                            onQuestionNumChanged) {
    // keep this up to date with new category additions
    const generateCategoryRemarks = ({questionType, categories, numOfQuestions}) => {
        if (categories.length === 0) {
            return 'You haven\'t picked any categories for your vocabulary!'
        }
        const pickedData = Object.values(pick(categoryToData, categories))
        console.log(pickedData)
        if (questionType === 'en-fr' || questionType === 'fr-en') {
            const termNum = sumBy(pickedData, ({rowCount}) => rowCount)
            console.log(termNum)
            if (termNum < numOfQuestions) {
                return "There are not enough terms in your selected categories to generate your questions."
            }
        } else if (questionType === 'fr_syn') {
            const synNum = sumBy(pickedData, ({synonymRowCount}) => synonymRowCount)
            if (synNum < numOfQuestions) {
                return "There are not enough terms with synonyms in your selected categories to generate your questions."
            }
        } else if (questionType === 'fr_ant') {
            const antNum = sumBy(pickedData, ({antonymRowCount}) => antonymRowCount)
            if (antNum < numOfQuestions) {
                return "There are not enough terms with antonyms in your selected categories to generate your questions."
            }
        }
        return false;
    }

    return (
        <>
            <Table
                dataSource={questionGenerators}
                pagination={false}
                rowKey={({key}) => key}
                footer={(currentPageData) =>
                    <Button
                        onClick={onQuestionCreated}
                        type={'primary'}
                    >
                        Add a question
                    </Button>}
            >
                <Col title='Question Type'
                     dataIndex='questionType'
                     key='questionType'
                     render={(questionType, {key}) =>
                         <Select
                             defaultValue={questionTypes[questionType]}
                             options={Object.keys(questionTypesReversed).map(value => ({value: value}))}
                             onChange={question => onParamChange('questionType')(key)(questionTypesReversed[question])}
                             style={{width: '100%'}}

                         />
                     }
                     width='20%'
                />
                <Col title='# of Questions'
                     dataIndex='numOfQuestions'
                     key='numOfQuestions'
                     width='5%'
                     render={(numOfQuestions, {key}) =>
                         <InputNumber
                             defaultValue={numOfQuestions}
                             min={0}
                             precision={0}
                             onChange={newNumOfQuestions => {
                                 onParamChange('numOfQuestions')(key)(newNumOfQuestions)
                                 onQuestionNumChanged()
                             }}
                             type={'number'}
                         />
                     }
                />
                <Col title='Categories'
                     dataIndex='categories'
                     key='categories'
                     width='75%'
                     render={(categories, entry) => {
                         const selectElement = <Select
                             allowClear={true}
                             defaultValue={categories}
                             mode={'multiple'}
                             style={{minWidth: '20vw'}}
                             tagRender={({value, closable, onClose}) => {
                                 const data = categoryToData[value]
                                 const tagParams = {
                                     color: data.color,
                                     key: value,
                                     closable: closable,
                                     onClose: onClose,
                                 }
                                 const tooltipParams = {
                                     placement: 'top',
                                     title: () => <List
                                         dataSource={[
                                             ['Number of Terms', data.rowCount],
                                             ['Number of Terms with Synonyms', data.synonymRowCount],
                                             ['Number of Terms with Antonyms', data.antonymRowCount],
                                         ]}
                                         renderItem={(entry) =>
                                             <Space split={' '}>
                                                 <Typography.Text>{entry[0]}:</Typography.Text>
                                                 <Typography.Text>{entry[1]}</Typography.Text>
                                             </Space>
                                         }
                                     >
                                     </List>
                                 }
                                 return (
                                     <Tooltip {...tooltipParams}>
                                         <Tag {...tagParams}>{value}</Tag>
                                     </Tooltip>
                                 )
                             }}
                             options={Object.entries(categoryToData).map(([key, value]) => ({'value': key}))}
                             onChange={onParamChange('categories')(entry.key)}
                             placeholder={'Select some categories!'}
                         >
                         </Select>
                         const categoryRemarks = generateCategoryRemarks(entry)

                         return <>
                             <Space>
                                 {selectElement}
                                 {categoryRemarks && <Tooltip
                                     placement={'top'}
                                     title={() =>
                                         <Typography.Text>
                                             {categoryRemarks}
                                         </Typography.Text>
                                     }
                                 >
                                     <WarningOutlined style={{color: colors.red, fontSize: '200%'}}/>
                                 </Tooltip>}
                             </Space>
                         </>
                     }}/>
                <Col
                    title=''
                    key='deleteAction'
                    render={(_, {key}) =>
                        <CloseCircleOutlined
                            twoToneColor={colors.red}
                            onClick={onQuestionDeleted(key)}
                        />
                    }
                />
            </Table>
        </>)
}