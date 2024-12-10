import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PostcardFormComponent } from './postcard-form.component';

describe('PostcardFormComponent', () => {
  let component: PostcardFormComponent;
  let fixture: ComponentFixture<PostcardFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PostcardFormComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PostcardFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
