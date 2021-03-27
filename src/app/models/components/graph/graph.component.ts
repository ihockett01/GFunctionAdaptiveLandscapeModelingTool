import { Component, OnInit, Inject } from '@angular/core';
import { ModelService } from '../../services/model.service';


@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.scss']
})
export class GraphComponent implements OnInit {

  constructor(
    private modelService:ModelService) { }

  

  showWiki() : void {
    
  }

  ngOnInit(): void {
    
  }

}
