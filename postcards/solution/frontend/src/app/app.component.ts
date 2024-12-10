import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { PostcardFormComponent } from './postcard-form/postcard-form.component';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, PostcardFormComponent, HttpClientModule ],
  providers: [],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'postcards';
}
