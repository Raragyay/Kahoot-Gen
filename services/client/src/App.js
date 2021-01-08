import './App.css';
import KahootSectionTable from "./components/KahootSectionTable";
import {Layout} from "antd";

const {Header, Content} = Layout;

function App() {
    return (
        <Layout>
            <Header>

            </Header>
            <Content
                style={{padding: '5vh 20vw 0'}}
            >
                <KahootSectionTable/>
            </Content>
        </Layout>
    );
}

export default App;
