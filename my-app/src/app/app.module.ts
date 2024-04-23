import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

@NgModule({
  declarations: [ //컴포넌트, 지시자, 파이프 등이 들어옴
    AppComponent
  ],
  imports: [ // 다른 모듈들이 들어옴
    BrowserModule,
    AppRoutingModule
  ],
  providers: [], //view가 없는 서비스 로직들이 들어옴
  bootstrap: [AppComponent] // 처음 실행할 컴포넌트 지정
})
export class AppModule { }
