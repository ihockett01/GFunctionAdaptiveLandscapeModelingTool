import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Routes, RouterModule } from '@angular/router';
import { MainComponent } from './main.component';
import { HttpClientModule } from '@angular/common/http';
import { GraphComponent } from './components/graph/graph.component';
import { WikiComponent } from './components/wiki/wiki.component';

const routes: Routes = [
  {
    path: 'main',
    component: MainComponent,
    children: [
      {
        path: 'graph',
        component: GraphComponent
      },
      {
        path: 'wiki',
        component: WikiComponent
      }
    ]
  }
];

@NgModule({
  declarations: [],
  imports: [CommonModule, RouterModule.forChild(routes), HttpClientModule],
  exports: [RouterModule]
})
export class HomeRoutingModule {}
