import React from 'react';
import {Table, Col, Tag, Select, InputNumber, Button} from 'antd';
import {CloseCircleOutlined} from "@ant-design/icons";
import {colors} from "../constants";

function KahootQuestionTable(questionGenerators,
                             categoryToColor,
                             questionTypes,
                             questionTypesReversed,
                             onParamChange,
                             onQuestionCreated,
                             onQuestionDeleted,
                             onQuestionNumChanged) {
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
                     render={(categories, {key}) => (<>
                         <Select
                             allowClear={true}
                             defaultValue={categories}
                             mode={'multiple'}
                             style={{minWidth: '50%'}}
                             tagRender={({value, closable, onClose}) => {
                                 const color = categoryToColor[value]
                                 const params = {
                                     color: color,
                                     key: value,
                                     closable: closable,
                                     onClose: onClose,
                                 }
                                 return (<Tag {...params}>{value}</Tag>)
                             }}
                             options={Object.entries(categoryToColor).map(([key, value]) => ({'value': key}))}
                             onChange={onParamChange('categories')(key)}
                             placeholder={'Select some categories!'}
                         >
                         </Select>
                     </>)}/>
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

export default KahootQuestionTable