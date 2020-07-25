import React from 'react';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import '../index.css';
class Home extends React.Component {
    render() {
        return (
            <Card>
                <CardContent>
                    React 및 Firebase 기반의 워드 클라우드 어플리케이션 웹앱
                </CardContent>
            </Card>
        );
    }
}

export default Home;