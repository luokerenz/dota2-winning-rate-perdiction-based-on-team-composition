package dota2KNN;

import java.util.ArrayList;

import net.sf.javaml.classification.Classifier;
import net.sf.javaml.classification.KNearestNeighbors;
import net.sf.javaml.core.Dataset;
import net.sf.javaml.core.Instance;

public class Estimater {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		ArrayList<Dataset> set = null;
		Dataset test = null;
		Preprocessor preprocessor = new Preprocessor();
		int num = 1275;
		try {
			preprocessor.grab("jdbc:mysql:", 10947, 1275);
			set = preprocessor.getData();
			test = preprocessor.getTestdata();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		for(int k=1;k<num*2;k=k+num/15)
		{
		Classifier knn = new KNearestNeighbors((int) (Math.sqrt(k)));
		knn.buildClassifier(set.get(set.size()-1));
		int correct = 0, wrong = 0;

		for (Instance inst : test) {
			Object predictedClassValue = knn.classify(inst);
			Object realClassValue = inst.classValue();
			try {
				if (predictedClassValue.equals(realClassValue))
					correct++;
				else
					wrong++;
			} catch (Exception e) {
			}
		}
		double p = (double) correct / (double) (correct + wrong);
		System.out.println(k/2+">"+p);
		}




	for(Dataset s:set)
		{
		Classifier knn = new KNearestNeighbors(213);
			knn.buildClassifier(s);
	int	correct = 0;
	int wrong = 0;
	for(Instance inst:test)
	{
			Object predictedClassValue = knn.classify(inst);
			Object realClassValue = inst.classValue();
			try {
				if (predictedClassValue.equals(realClassValue))
					correct++;
				else
					wrong++;
			} catch (Exception e) {
			}
	}
	 System.out.println((correct+wrong)/2+">"+(double)correct/(double)(correct+wrong));
		}
}
}
