import './styles/App.less';
import KahootSectionTable from "./components/KahootSectionTable";
import {Divider, Layout, Space, Typography} from "antd";
import {Footer} from "antd/es/layout/layout";
import {GithubOutlined} from "@ant-design/icons";

const {Header, Content} = Layout;

function App() {
    return (
        <Layout>
            <Header>
                <img
                    className={'logoImage'}
                    src={'logolong.png'}
                    alt={'logo'}/>
            </Header>
            <Content
                className={'mainContent'}
            >
                <KahootSectionTable/>
            </Content>
            <Footer style={{textAlign: 'center'}}>
                <Space split={<Divider type={'vertical'}/>}>
                    <Typography.Text>Created with React and Ant Design</Typography.Text>
                    <Typography.Link href={'https://github.com/Raragyay/Kahoot-Gen'}><GithubOutlined/></Typography.Link>
                </Space>
            </Footer>
        </Layout>
    );
}

export default App;
